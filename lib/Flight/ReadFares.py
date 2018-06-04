
import psycopg2

from BarsLog import printlog


def ReadCityPairs(conn, departure_airport=None, arrival_airport=None):
    """Read city pairs."""
    RcpSql = """
        SELECT city_pair, start_city, end_city, pair_indicator, distance,
        baggage_alownce, pair_rule_no, remarks
    FROM city_pair"""
    if departure_airport is not None and arrival_airport is not None:
        RcpSql += """
            WHERE start_city = '%s'
            AND end_city = '%s'""" \
            % (departure_airport, arrival_airport)

    printlog(2, "%s" % RcpSql)
    cur = conn.cursor()
    cur.execute(RcpSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print item,
        print

    cur.close()


def ReadFareSegments(conn):
    """Read fare segments."""
    RfSql = """
    SELECT company_code, fare_code, city_pair, valid_from_date, valid_to_date,
        fare_value, active_flag
    FROM fare_segm"""

    printlog(2, "%s" % RfSql)
    cur = conn.cursor()
    cur.execute(RfSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print item,
        print

    cur.close()


def ReadFareCodes(conn):
    """Read fare codes."""
    RfSql = """
        SELECT
        company_code, fare_code, short_description, description,
        selling_class, fare_category, onw_return_flag
    FROM fare_codes"""

    printlog(2, "%s" % RfSql)
    cur = conn.cursor()
    cur.execute(RfSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print item,
        print

    cur.close()
