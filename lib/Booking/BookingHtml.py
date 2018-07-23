"""
Display booking in HTML format.
"""

from BarsLog import blogger
from Booking.FareCalcDisplay import FareCalcDisplay, ReadSellingConfig
from Flight.AvailDb import ReadAvailDb, get_avail_flights, get_selling_conf
from Flight.ReadTaxes import ApplyTaxes, ReadTaxes
from Ssm.SsmDb import GetCityPair
from Flight.ReadFlights import ReadFlightDeparture
from Booking.BookingInfo import AddBook, AddBookCrossIndex, AddItinerary, \
    AddPassenger, AddContact, AddBookRequests, AddBookTimeLimit, \
    AddBookingFareSegments, AddPayment, AddBookFares, AddBookFaresPayments, \
    AddBookFaresPayments, AddBookFarePassengers, UpdateBookPayment
from Booking.ReadItinerary import ReadItinerary, UpdateBook, UpdateItinerary
from Booking.ReadBooking import ReadPassengers


def GetAvailHtml(conn, flightDate, flightDate2,
                 departAirport, arriveAirport,
                 vCompany, flightUrl=None):
    """Get availability information."""
    blogger().debug("Get availability for depart %s arrive %s date %s"
                  % (departAirport, arriveAirport, flightDate))
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    flights = ReadAvailDb(conn, vCompany, flightDate, cityPairNo,
                          departAirport, arriveAirport)
    selling_classes = get_selling_conf(conn, vCompany)
    # for flight in flights:
        #flight.display()
    rbuf = "<table>"
    for selling_class in selling_classes:
        flights = get_avail_flights(conn, flightDate, flightDate2, cityPairNo,
                                    departAirport, arriveAirport,
                                    selling_class[0], vCompany)
        for flight in flights:
            rbuf += flight.html(flightUrl)
    rbuf += "</table>"
    return rbuf


def GetPriceHtml(conn,
                 aCompanyCode,
                 departAirport, arriveAirport,
                 flightDate, flightDate2,
                 selling_class, onw_return_ind, fare_category, authority_level):
    """Read and display price information."""
    blogger().debug("Get price for depart %s arrive %s class %s on %s"
                  % (departAirport, arriveAirport, selling_class, flightDate))
    rbuf = "<table>\n"
    sellconfigs = ReadSellingConfig(conn, aCompanyCode)
    rbuf += "<!-- %d selling configurations -->\n" % len(sellconfigs)
    # for flightClass in sorted(sellconfigs, key=sellconfigs.get, reverse=False):
        # sellconfigs[flightClass].display()
    cityPairNo = GetCityPair(conn, departAirport, arriveAirport)
    blogger().debug("Get price for city pair %d class %s on %s"
                  % (cityPairNo, selling_class, flightDate))
    taxes = ReadTaxes(conn, aCompanyCode, flightDate, flightDate2,
                      departAirport,
                      pass_code1='ADULT', pass_code2='CHILD',
                      aState='GP', aNation='ZA',
                      aReturnInd='O')
    rbuf += "<!-- %d taxes -->\n" % len(taxes)
    total_amount = 0.0
    for flightClass in sorted(sellconfigs, key=sellconfigs.get, reverse=False):
        fare_factor = float(sellconfigs[flightClass].fare_factor)
        fares = FareCalcDisplay(conn,
                                aCompanyCode,
                                cityPairNo,
                                taxes,
                                flightDate,
                                flightDate2,
                                flightClass,
                                onw_return_ind,
                                fare_category,
                                authority_level,
                                flightDate2,
                                fare_factor)
        for fare in fares:
            if fare.selling_class == selling_class:
                fare.apply_taxes(taxes)
                total_amount += fare.total_amount
                rbuf += fare.html()
    rbuf += "</table>\n"
    return rbuf, round(total_amount, 2)


def PutBookHtml(conn, vCompany, vBookCategory, vOriginAddress,
                vOriginBranchCode, vAgencyCode,
                groupName, paxRecs,
                aCurrency, payAmount,
                flightNumber, flightDate,
                departAirport, arriveAirport,
                sellClass, aFareBasis,
                aTimeLimit,
                vUser, vGroup):
    """Make a booking."""
    if paxRecs is None:
        msg = "<p/>No passenger names"
        return 0, '', msg
    blogger().debug("Book fare basis %s payment %s%.2f flight %s date %s"
                  % (aFareBasis, aCurrency, payAmount, flightNumber,
                     flightDate))
    vSeatQuantity = len(paxRecs)
    if payAmount is None:
        payAmount = 0.0
    if sellClass is None:
        sellClass = 'Y'
    #if departAirport is None or arriveAirport is None:
        #blogger().info("Flight number and date must be specified")
        #return
    blogger().debug("Book %d seats on flight %s date %s class %s"
                  % (vSeatQuantity, flightNumber, flightDate, sellClass))
    n, fd = ReadFlightDeparture(conn, sellClass, flightNumber, flightDate)
    if n == 0:
        msg = "<p/>Flight number and date not found"
        return 0, '', msg
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
            flightDate, groupName, vUser, vGroup)
    AddItinerary(conn, bn, flightNumber, flightDate,
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
                           flightNumber, flightDate,
                           flightDate, flightDate,
                           sellClass, aFareBasis,
                           aCurrency, payAmount,
                           vUser, vGroup)
    conn.commit()
    blogger().info("Booking reference %s" % pnr)
    msg = "<p/>Booking reference %s" % pnr
    return bn, pnr, msg


def PutPayHtml(conn, aBookNo, aSellClass,
               aCurrency, aPayAmount, aPayAmount2,
               aCompany, aOriginBranchCode, aFareBasisCode,
               vPaymentType, vPaymentForm, vDocNum,
               aUser, aGroup):
    """Process payment."""
    if aBookNo is None:
        blogger().error("Book number not specified")
        msg = "<p/>Book number not specified"
        return 1, msg
    blogger().info("Process payment of %s%.2f for book %d"
                 % (aCurrency, aPayAmount, aBookNo))
    paxRecs = ReadPassengers(conn, aBookNo)
    blogger().info("Read %d passengers" % len(paxRecs))
    # itenRecs = GetItinerary(conn, aBookNo)
    vPaymentMode = ' '
    vRemark = ' '
    vFareNo = 1
    AddPayment(conn, vPaymentForm, vPaymentType, aCurrency, int(aPayAmount),
               vDocNum, vPaymentMode,
               aBookNo, paxRecs[0].passenger_name, paxRecs[0].passenger_code,
               aOriginBranchCode, vRemark,
               aUser, aGroup)
    # payAmounts = [int(aPayAmount*100), int(aPayAmount2*100)]
    payAmounts = [aPayAmount, aPayAmount2]
    irecs = ReadItinerary(conn, aBookNo, None, None,
                          fnumber=None, start_date=None, end_date=None)
    if len(irecs) > 2:
        blogger().info("Found %d itenaries" % len(irecs))
        msg = "<p/>Found %d itenaries" % len(irecs)
        return 1, msg
    else:
        n = 0
        totalPayment = 0
        for irec in irecs:
            irec.blog()
            AddBookFares(conn, aBookNo, vFareNo, paxRecs[0].passenger_code,
                         irec.departure_airport, irec.arrival_airport,
                         aCurrency, payAmounts[n], aUser, aGroup)
            AddBookFaresPayments(conn, aBookNo, vFareNo,
                                 paxRecs[0].passenger_code, aFareBasisCode,
                                 aCurrency, payAmounts[n],
                                 aUser, aGroup)
            totalPayment += payAmounts[n]
            n += 1
        AddBookFarePassengers(conn, aBookNo, paxRecs[0].passenger_code,
                              aCurrency, totalPayment,
                              aUser, aGroup)
    UpdateBookPayment(conn, aBookNo, aCurrency, totalPayment)
    UpdateItinerary(conn, aBookNo, 'A')
    UpdateBook(conn, aBookNo, 'A')
    conn.commit()
    blogger().info("Payment approved")
    msg = "<p/>Payment approved."
    return 0, msg
