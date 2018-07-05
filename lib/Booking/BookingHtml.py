"""
Display booking in HTML format.
"""

from Flight.AvailDb import get_selling_conf, get_avail_flights, OldAvailSvc
from Flight.ReadTaxes import ReadTaxes, ApplyTaxes
from Booking.FareCalcDisplay import FareCalcDisplay, ReadPayments, \
     ReadSellingConfig, GetPriceSsr
from Ssm.SsmDb import GetCityPair
from BarsLog import printlog


def GetAvailHtml(conn, dt1, dt2, cityPairNo,
                 departAirport, arriveAirport,
                 selling_classes, vCompany):
    """Get availability information."""
    flights = OldAvailSvc(conn, vCompany, dt1, cityPairNo,
                          departAirport, arriveAirport)
    for flight in flights:
        flight.display()
    rbuf = "<table>"
    for selling_class in selling_classes:
        flights = get_avail_flights(conn, dt1, dt2, cityPairNo,
                                    departAirport, arriveAirport,
                                    selling_class[0], vCompany)
        for flight in flights:
            rbuf += flight.html()
    rbuf += "</table>"
    return rbuf


def GetPriceHtml(conn,
                 aCompanyCode,
                 departAirport, arriveAirport,
                 dt1, dt2,
                 selling_class, onw_return_ind, fare_category, authority_level):
    """Read and display price information."""
    rbuf = "<table>\n"
    sellconfigs = ReadSellingConfig(conn, aCompanyCode)
    # for cls in sorted(sellconfigs, key=sellconfigs.get, reverse=False):
        # sellconfigs[cls].display()
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    printlog(1, "Get price for city pair %d class %s on %s"
             % (cityPairNo, selling_class, dt1))
    taxes = ReadTaxes(conn, aCompanyCode, dt1, dt2, departAirport,
                      pass_code1='ADULT', pass_code2='CHILD',
                      aState='GP', aNation='ZA',
                      aReturnInd='O')
    for cls in sorted(sellconfigs, key=sellconfigs.get, reverse=False):
        fare_factor = float(sellconfigs[cls].fare_factor)
        fares = FareCalcDisplay(conn,
                                aCompanyCode,
                                cityPairNo,
                                taxes,
                                dt1,
                                dt2,
                                cls,
                                onw_return_ind,
                                fare_category,
                                authority_level,
                                dt2,
                                fare_factor)
        for fare in fares:
            if fare.selling_class == selling_class:
                fare.apply_taxes(taxes)
                rbuf += fare.html()
    rbuf += "</table>\n"
    return rbuf
