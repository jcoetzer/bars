# @file ReadItenary.py
"""
Read itenary.
"""

import sys
import operator
import psycopg2
import datetime
from BarsLog import set_verbose, get_verbose, printlog
from Booking.ItenaryData import ItenaryData


def ReadItenary(conn, bookno, booking_status, action_codes,
                fnumber=None, start_date=None, end_date=None):
    """Read itenary."""
    itenaryrecs = []

    itenSql = \
        "SELECT flight_number,flight_date,selling_class,departure_airport," \
        "arrival_airport,itenary_stat_flag,reserve_status,itenary_type" \
        " FROM itenary" \
        " WHERE book_no=%d" \
        % int(bookno)
    if booking_status == 'A' or booking_status == 'Y':
        itenSql += \
            " AND itenary_stat_flag='A' and itenary_type='R'"
        if len(action_codes):
            itenSql += \
                " AND reserve_status[1,2] IN (%s)" % action_codes
    elif booking_status == 'X':
        # itenSql += \
            # " AND itenary_stat_flag!='A' and itenary_type='R'"
        pass
    elif booking_status == '*':
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
        itenaryrecs.append(ItenaryData(row['flight_number'],
                                       row['flight_date'],
                                       row['selling_class'],
                                       row['departure_airport'],
                                       row['arrival_airport'],
                                       row['itenary_stat_flag'],
                                       row['reserve_status'],
                                       row['itenary_type']))
    cur.close()
    return itenaryrecs
