# @file ReadFlightBookings.py
"""
Read booking e.a. for flights.
"""

import psycopg2
import psycopg2.extras
from BarsLog import printlog


def ReadFlightBookings(conn, flight_number, board_date):
    """Read bookings for flight."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    printlog(1, "Flight %s board %s bookings"
             " [flight_segm_date,itenary,book,action_codes]"
             % (flight_number, board_date))
    FbSql = \
        """SELECT DISTINCT it.book_no itbn, bo.origin_address booa,
            it.departure_airport itda, it.arrival_airport itaa,
            it.departure_time itdt, it.arrival_time itat, it.request_nos itrn,
            it.selling_class itsc, bo.no_of_seats bons, group_name bogn
        FROM itenary it, book bo
             WHERE it.flight_number='%s' AND it.flight_date='%s'
             AND bo.book_no = it.book_no""" \
        % (flight_number, board_date)
    printlog(2, FbSql)
    cur.execute(FbSql)
    npax = 0
    for row in cur:
        book_no = row['itbn']
        departure_time = str(row['itdt'].strftime("%H:%M") or '')
        arrival_time = str(row['itat'].strftime("%H:%M") or '')
        print("%8s %6s %3s %3s %6s %6s %1s %10s %5s %s"
              % (book_no, row['booa'], row['itda'], row['itaa'],
                 departure_time, arrival_time,
                 row['itsc'], str(row['itrn'] or ''),
                 row['bons'], str(row['bogn'] or '')))
        FbSql2 = \
            """SELECT pa.pax_name papn,
            pa.request_nos parn, pa.pax_no papr, pa.pax_code papc
            FROM passenger pa
            WHERE pa.book_no = %d
            AND pa.pax_no > 0
            AND pa.pax_code <> 'INF'
            """ % book_no
        printlog(2, FbSql2)
        cur2.execute(FbSql2)
        for row2 in cur2:
            print("\t %3s %s %s %s"
                  % (str(row2['papr'] or ''), row2['papn'], str(row2['parn'] or ''),
                     row2['papc']))
            npax += 1
    cur2.close()
    cur.close()
    print("Flight %s on %s has %d passengers"
          % (flight_number, board_date, npax))


def ReadFlightContacts(conn, flight_number, board_date):
    """Read contact info for flight."""
    print("Itenary for flight %s board %s passenger contact [itenary]"
          % (flight_number, board_date))
    FbSql = \
        """SELECT email_address, contact_phone_no
        FROM pax_contact WHERE book_no IN
            (SELECT DISTINCT book_no FROM itenary
             WHERE flight_number='%s' AND flight_date='%s')""" \
        % (flight_number, board_date)
    printlog(2, FbSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(FbSql)
    for row in cur:
        contact_phone_no = str(row['contact_phone_no'] or '')
        email_address = str(row['email_address'] or '')
        if len(contact_phone_no) > 0 and len(contact_phone_no) > 0:
            print("%20s,%s" % (contact_phone_no, email_address))
