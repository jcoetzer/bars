# @file SsmDb.py
"""
SSM data as stored in database.
"""

import logging

logger = logging.getLogger("web2py.app.bars")


def GetConfigTableNo(conn, aAircraftCode):
    """Read configuration table number."""
    cfgn = None
    logger.debug("Read configuration for %s" % aAircraftCode)
    cur = conn.cursor()
    ssmSql = \
        """SELECT config_table, selling_class, seat_capacity
        FROM aircraft_config
        WHERE aircraft_code = '%s'
        ORDER BY seat_capacity DESC""" \
        % aAircraftCode
    logger.debug("%s" % ssmSql)
    cur.execute(ssmSql)

    for row in cur:
        cfgn = str(row[0])
        logger.info("Config %s class %s seats %d" % (row[0], row[1], row[2]))
        # TODO first one only, for now
        break

    cur.close()
    return cfgn


def GetCityPair(conn, depart_airport, arrive_airport):
    """Read city pair number."""
    #logger.debug("Read city pair %s and %s"
                  #% (depart_airport, arrive_airport))
    cur = conn.cursor()
    ssmSql = \
        "SELECT city_pair FROM city_pairs" \
        " WHERE departure_airport='%s' AND arrival_airport='%s'" \
        % (depart_airport, arrive_airport)
    #logger.debug("%s" % ssmSql)
    cur.execute(ssmSql)

    city_pair_id = 0
    for row in cur:
        city_pair_id = row[0]

    #logger.info("City pair %d" % city_pair_id)

    return int(city_pair_id)


def CheckCityPair(conn, depart_airport, arrive_airport, pair_rule_no,
                  userName, groupName):
    """Read city pair number."""
    logger.debug("Check city pair %s and %s"
                  % (depart_airport, arrive_airport))
    cur = conn.cursor()
    ssmSql = \
        "SELECT city_pair FROM city_pairs" \
        " WHERE departure_airport='%s' AND arrival_airport='%s'" \
        % (depart_airport, arrive_airport)
    logger.debug("%s" % ssmSql)
    cur.execute(ssmSql)

    city_pair_id = 0
    for row in cur:
        city_pair_id = row[0]
        logger.info("City pair %d" % city_pair_id)

    cur.close()
    return city_pair_id


def CheckFlightPeriod(conn, ssm):
    """Check flight period."""
    logger.debug("Check flight %s period %s to %s"
                  % (ssm.flight_number, ssm.start_date.strftime("%Y-%m-%d"),
                     ssm.end_date.strftime("%Y-%m-%d")))
    ssmSql = "SELECT start_date, end_date, schedule_period_no" \
             " FROM flight_periods" \
             " WHERE flight_number='%s'" \
             " AND (start_date>='%s' OR end_date<='%s')" \
             % (ssm.flight_number, ssm.start_date.strftime("%Y-%m-%d"),
                ssm.end_date.strftime("%Y-%m-%d"))
    logger.debug("%s" % ssmSql)
    cur = conn.cursor()
    cur.execute(ssmSql)

    flight_period_id = 0
    sdate = None
    edate = None
    for row in cur:
        sdate = row[0]
        edate = row[1]
        flight_period_id = row[2]
        logger.info("Start %s end %s schedule period %d"
                      % (sdate, edate, flight_period_id))

    cur.close()
    return flight_period_id, sdate, edate


def CheckAircraftConfig(conn, ssm):
    """Read aircraft configuration."""
    logger.debug("Read aircraft %s configuration" % ssm.aircraft_tail)
    ssmSql = "SELECT DISTINCT aircraft_config_id,aircraft_code" \
             " FROM aircraft_config" \
             " WHERE aircraft_tail='%s'" \
             % (ssm.aircraft_tail)
    logger.debug("%s" % ssmSql)
    cur = conn.cursor()
    cur.execute(ssmSql)

    aircraft_config_id = 0
    aircraft_code = None
    for row in cur:
        aircraft_config_id = row[0]
        aircraft_code = row[1]
        logger.info("Aircraft code %s" % aircraft_code)

    return aircraft_config_id, aircraft_code
