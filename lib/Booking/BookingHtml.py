"""
Display booking in HTML format.
"""

from Flight.AvailDb import get_selling_conf, get_avail_flights, OldAvailSvc


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
