"""
Check flight date leg.
"""
import sys
import logging
import psycopg2
from psycopg2 import extras

from ReadDateTime import ReadDate

logger = logging.getLogger("web2py.app.bars")


def ReadFlightDateLegId(conn, fli):
    """Check flight date leg."""
    flight_numbers = []
    flight_dates = []
    print("Flight date legs for flight leg ID %d [flight_date_leg]" % (fli))
    RcSql = \
        "SELECT flight_date_leg_id,trim(flight_number) fn,board_date,departure_time," \
        " departure_airport,arrival_airport,leg_number,update_user,update_time" \
        " FROM flight_date_leg WHERE flight_date_leg_id=%d"  \
        % (fli)
    logger.info(RcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RcSql)
    n = 0
    for row in cur:
        fli = int(row['flight_date_leg_id'] or 0)
        flight_numbers.append(row['fn'])
        flight_dates.append(row['board_date'])
        print("\tleg id %d flight %s date %s depart %s time %s arrive %s leg %d user %s update %s"
              % (fli, str(row['fn'] or ''), row['board_date'],
                 row['departure_airport'],
                 row['departure_time'].isoformat().split("T")[1][0:5],
                 row['arrival_airport'], row['leg_number'],
                 row['update_user'], row['update_time']))
        n += 1

    if n == 0:
        print("\t not found")

    return flight_numbers, flight_dates
