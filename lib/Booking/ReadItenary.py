# @file ReadItenary.py
"""
Read itinerary.
"""

import sys
import operator
import psycopg2
import datetime
from BarsLog import set_verbose, get_verbose, printlog
from Booking.ItenaryData import ItenaryData


def ReadItenary(conn, bookno, status_flag, action_codes,
                fnumber=None, start_date=None, end_date=None):
    """Read itinerary."""
    itineraryrecs = []

    itenSql = \
        "SELECT flight_number,flight_date,selling_class,departure_airport," \
        "city_pair," \
        "arrival_airport,status_flag,reserve_status,itinerary_type" \
        " FROM itineraries" \
        " WHERE book_no=%d" \
        % int(bookno)
    if status_flag == 'A' or status_flag == 'Y':
        itenSql += \
            " AND status_flag='A' and itinerary_type='R'"
        if len(action_codes):
            itenSql += \
                " AND reserve_status[1,2] IN (%s)" % action_codes
    elif status_flag == 'X':
        # itenSql += \
            # " AND status_flag!='A' and itinerary_type='R'"
        pass
    elif status_flag == '*':
        pass
    else:
        pass
    if start_date is not None and end_date is not None:
        itenSql += \
            " AND flight_date>='%s' AND flight_date<='%s'" \
            % (start_date, end_date)
    if fnumber is not None and ('%' in fnumber or '_' in fnumber):
        itenSql += \
            " AND flight_number like '%s'" % fnumber
    itenSql += \
        " ORDER BY flight_date,departure_time ASC"
    printlog(2, itenSql)
    sys.stdout.flush()
    n_itens = 0
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(itenSql)
    for row in cur:
        itineraryrecs.append(ItenaryData(row['flight_number'],
                                       row['flight_date'],
                                       row['selling_class'],
                                       row['departure_airport'],
                                       row['arrival_airport'],
                                       row['city_pair'],
                                       row['status_flag'],
                                       row['reserve_status'],
                                       row['itinerary_type']))
    cur.close()
    return itineraryrecs


def UpdateItenary(conn, aBookNo, aStatus='A'):
    """Activate itinerary."""
    printlog(1, "Set bookings %d itinerary status to %s" % (aBookNo, aStatus))
    UaSql = """UPDATE itineraries
               SET (status_flag, processing_flag)
                 = ('%s', 'Y')
               WHERE book_no = %d""" \
            % (aStatus, aBookNo)
    cur = conn.cursor()
    printlog(2, UaSql)
    cur.execute(UaSql)
    printlog(2, "Updated %d rows" % cur.rowcount)


def UpdateBook(conn, aBookNo, aStatus='A'):
    """Activate itinerary."""
    printlog(1, "Set bookings %d status to %s" % (aBookNo, aStatus))
    UaSql = """UPDATE bookings SET status_flag='%s'
            WHERE book_no = %d""" % (aStatus, aBookNo)
    cur = conn.cursor()
    printlog(2, UaSql)
    cur.execute(UaSql)
    printlog(2, "Updated %d rows" % cur.rowcount)
