# @file ReadFares.py
"""
Read fares and stuff.
"""
import logging
import psycopg2
from psycopg2 import extras


logger = logging.getLogger("web2py.app.bars")


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

    logger.debug("%s" % RcpSql)
    cur = conn.cursor()
    cur.execute(RcpSql)

    logger.debug("Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print(item),
        print

    cur.close()


def ReadFareSegments(conn):
    """Read fare segments."""
    logger.info("Fare segments:")
    RfSql = """
    SELECT company_code, fare_basis_code, city_pair, valid_from_date, valid_to_date,
        fare_amount, active_flag
    FROM fare_segments"""

    logger.debug("%s" % RfSql)
    cur = conn.cursor()
    cur.execute(RfSql)

    logger.debug("Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print(item),
        print

    cur.close()


def ReadFareCodes(conn):
    """Read fare codes."""
    """Read fare segments."""
    logger.info("Fare codes:")
    RfSql = """
        SELECT
        company_code, fare_basis_code, short_description, description,
        selling_class, fare_category, oneway_return_flag
    FROM fare_basis_codes"""

    logger.debug("%s" % RfSql)
    cur = conn.cursor()
    cur.execute(RfSql)

    logger.debug("Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        for item in row:
            print(item),
        print

    cur.close()
