# @file ReadFares.py
"""
Read fares and stuff.
"""
import psycopg2

from BarsLog import printlog


def ReadCityPairs(conn, departure_airport=None, arrival_airport=None):
    """Read city pairs."""
    RcpSql = """
        SELECT city_pair, departure_city, arrival_airport, pair_indicator,
        distance, baggage_alownce, pair_rule_no, remarks
    FROM city_pairs"""
    if departure_airport is not None and arrival_airport is not None:
        RcpSql += """
            WHERE departure_city = '%s'
            AND arrival_airport = '%s'""" \
            % (departure_airport, arrival_airport)

    printlog(2, "%s" % RcpSql)
    cur = conn.cursor()
    cur.execute(RcpSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print(item, end=' ')
        print

    cur.close()


def ReadFareSegments(conn):
    """Read fare segments."""
    printlog(1, "Fare segments:")
    RfSql = """
    SELECT company_code, fare_basis_code, city_pair, valid_from_date, valid_to_date,
        fare_amount, active_flag
    FROM fare_segments"""

    printlog(2, "%s" % RfSql)
    cur = conn.cursor()
    cur.execute(RfSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print(item, end=' ')
        print

    cur.close()


def ReadFareCodes(conn):
    """Read fare codes."""
    """Read fare segments."""
    printlog(1, "Fare codes:")
    RfSql = """
        SELECT
        company_code, fare_basis_code, short_description, description,
        selling_class, fare_category, onw_return_flag
    FROM fare_basis_codes"""

    printlog(2, "%s" % RfSql)
    cur = conn.cursor()
    cur.execute(RfSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print(item, end=' ')
        print

    cur.close()
