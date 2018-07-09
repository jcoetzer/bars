"""
Display booking in HTML format.
"""

from BarsLog import printlog
from Booking.FareCalcDisplay import FareCalcDisplay, ReadSellingConfig
from Flight.AvailDb import OldAvailSvc, get_avail_flights, get_selling_conf
from Flight.ReadTaxes import ApplyTaxes, ReadTaxes
from Ssm.SsmDb import GetCityPair


def GetAvailHtml(conn, dt1, dt2,
                 departAirport, arriveAirport,
                 vCompany):
    """Get availability information."""
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    flights = OldAvailSvc(conn, vCompany, dt1, cityPairNo,
                          departAirport, arriveAirport)
    selling_classes = get_selling_conf(conn, vCompany)
    # for flight in flights:
        #flight.display()
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
    rbuf += "<!-- %d selling configurations -->\n" % len(sellconfigs)
    # for clas in sorted(sellconfigs, key=sellconfigs.get, reverse=False):
        # sellconfigs[clas].display()
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    printlog(1, "Get price for city pair %d class %s on %s"
             % (cityPairNo, selling_class, dt1))
    taxes = ReadTaxes(conn, aCompanyCode, dt1, dt2, departAirport,
                      pass_code1='ADULT', pass_code2='CHILD',
                      aState='GP', aNation='ZA',
                      aReturnInd='O')
    rbuf += "<!-- %d taxes -->\n" % len(taxes)
    for clas in sorted(sellconfigs, key=sellconfigs.get, reverse=False):
        fare_factor = float(sellconfigs[clas].fare_factor)
        fares = FareCalcDisplay(conn,
                                aCompanyCode,
                                cityPairNo,
                                taxes,
                                dt1,
                                dt2,
                                clas,
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
