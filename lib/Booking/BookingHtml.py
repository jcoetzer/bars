"""
Display booking in HTML format.
"""

from BarsLog import printlog
from Booking.FareCalcDisplay import FareCalcDisplay, ReadSellingConfig
from Flight.AvailDb import ReadAvailDb, get_avail_flights, get_selling_conf
from Flight.ReadTaxes import ApplyTaxes, ReadTaxes
from Ssm.SsmDb import GetCityPair
from Flight.ReadFlights import ReadFlightDeparture
from Booking.BookingInfo import AddBook, AddBookCrossIndex, AddItinerary, \
    AddPassenger, AddContact, AddBookRequests, AddBookTimeLimit, \
    AddBookingFareSegments


def GetAvailHtml(conn, dt1, dt2,
                 departAirport, arriveAirport,
                 vCompany, flightUrl=None):
    """Get availability information."""
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    flights = ReadAvailDb(conn, vCompany, dt1, cityPairNo,
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
            rbuf += flight.html(flightUrl)
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
    logger.debug("Get price for city pair %d class %s on %s"
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


def PutBookHtml(conn, vCompany, vBookCategory, vOriginAddress,
                vOriginBranchCode, vAgencyCode,
                groupName, paxRecs,
                aCurrency, payAmount,
                flightNumber, dt1,
                departAirport, arriveAirport,
                sellClass, aFareBasis,
                aTimeLimit,
                vUser, vGroup):
    """Make a booking."""
    if paxRecs is None:
        msg = "No passenger names"
        return msg
    logger.debug("Book fare basis %s payment %s%.2f flight %s date %s"
             % (aFareBasis, aCurrency, payAmount, flightNumber, dt1))
    vSeatQuantity = len(paxRecs)
    if payAmount is None:
        payAmount = 0.0
    if sellClass is None:
        sellClass = 'Y'
    #if departAirport is None or arriveAirport is None:
        #print("Flight number and date must be specified")
        #return
    logger.debug("Book %d seats on flight %s date %s class %s"
             % (vSeatQuantity, flightNumber, dt1, sellClass))
    n, fd = ReadFlightDeparture(conn, sellClass, flightNumber, dt1)
    if n == 0:
        msg = "Flight number and date not found"
        return msg
    departAirport = fd.departure_airport
    arriveAirport = fd.arrival_airport
    cityPairNo = fd.city_pair
    departTerm = fd.departure_terminal
    arriveTerm = fd.arrival_terminal
    departTime = fd.departure_time
    arriveTime = fd.arrival_time
    bn, pnr = AddBookCrossIndex(conn, vBookCategory, vOriginAddress,
                                vUser, vGroup)
    AddBook(conn, bn, pnr, vSeatQuantity, vOriginAddress, vBookCategory,
            vOriginBranchCode, vAgencyCode,
            dt1, groupName, vUser, vGroup)
    AddItinerary(conn, bn, flightNumber, dt1,
                 departAirport, arriveAirport,
                 departTime, arriveTime,
                 departTerm, arriveTerm,
                 cityPairNo, sellClass,
                 vUser, vGroup)
    AddPassenger(conn, bn, paxRecs, vUser, vGroup)
    AddContact(conn, bn, paxRecs, vUser, vGroup)
    paxRequests = []
    for paxRec in paxRecs:
        paxRequests.append(paxRec.date_of_birth.strftime("%d%b%Y").upper())
    AddBookRequests(conn, bn, vCompany, 'CKIN', paxRequests, vUser, vGroup)
    AddBookTimeLimit(conn, bn, vAgencyCode, vUser, vGroup)
    AddBookingFareSegments(conn, bn, 1, paxRecs[0].passenger_code,
                           departAirport, arriveAirport,
                           flightNumber, dt1,
                           dt1, dt1,
                           sellClass, aFareBasis,
                           aCurrency, payAmount,
                           vUser, vGroup)
    msg = "<p/>Booking reference %s" % pnr
    return bn, pnr
