# @file SsmDb.py
#

from BarsLog import printlog


def GetConfigTableNo(conn, aAircraftCode):
    """Read configuration table number."""
    cfgn = None

    cur = conn.cursor()
    ssmSql = \
        "SELECT config_table_no,selling_cls_code,seat_capacity " \
        "FROM aircraft_config " \
        "WHERE aircraft_code = '%s' ORDER BY seat_capacity DESC" % aAircraftCode
    printlog(2, "%s" % ssmSql)
    cur.execute(ssmSql)

    for row in cur:
        cfgn = str(row[0])
        printlog(1, "Config %s class %s seats %d" % (row[0], row[1], row[2]))
        # TODO first one only, for now
        break

    cur.close()
    return cfgn


def GetCityPair(conn, depart_airport, arrive_airport):
    """Read city pair number."""
    cur = conn.cursor()
    ssmSql = \
        "SELECT city_pair_no FROM city_pair" \
        " WHERE start_city='%s' AND end_city='%s'" \
        % (depart_airport, arrive_airport)
    printlog(2, "%s" % ssmSql)
    cur.execute(ssmSql)

    city_pair_id = 0
    for row in cur:
        city_pair_id = row[0]

    printlog(1, "City pair %d" % city_pair_id)

    return int(city_pair_id)


def CheckCityPair(conn, depart_airport, arrive_airport, pair_rule_no, userName, groupName):
    """Read city pair number."""
    cur = conn.cursor()
    ssmSql = \
        "SELECT city_pair_no FROM city_pair" \
        " WHERE start_city='%s' AND end_city='%s'" \
        % (depart_airport, arrive_airport)
    printlog(2, "%s" % ssmSql)
    cur.execute(ssmSql)

    city_pair_id = 0
    for row in cur:
        city_pair_id = row[0]
        printlog(1, "City pair %d" % city_pair_id)

    if city_pair_id == 0:
        ssmSql = \
            "INSERT INTO city_pair(start_city, end_city, pair_indicator, pair_rule_no, user_name, user_group)" \
            " VALUES ('%s', '%s', 'A', %d, '%s', '%s') RETURNING city_pair_no" \
            % (depart_airport, arrive_airport, pair_rule_no, userName, groupName)
        printlog(2, "%s" % ssmSql)
        cur.execute(ssmSql)
        for row in cur:
            city_pair_id = row[0]
            printlog(1, "New city pair %d" % city_pair_id)

    cur.close()
    return city_pair_id


def CheckFlightPeriod(conn, ssm):
    """Check flight period."""
    ssmSql = "SELECT start_date, end_date, schd_perd_no" \
             " FROM flight_periods" \
             " WHERE flight_number='%s'" \
             " AND (start_date>='%s' OR end_date<='%s')" \
             % (ssm.flight_number, ssm.start_date.strftime("%Y-%m-%d"), ssm.end_date.strftime("%Y-%m-%d"))
    printlog(2, "%s" % ssmSql)
    cur = conn.cursor()
    cur.execute(ssmSql)

    flight_period_id = 0
    sdate = None
    edate = None
    for row in cur:
        sdate = row[0]
        edate = row[1]
        flight_period_id = row[2]
        printlog(1, "Start %s end %s schedule period %d" % (sdate, edate, flight_period_id))

    cur.close()
    return flight_period_id, sdate, edate


def CheckAircraftConfig(conn, ssm):
    """Read aircraft configuration."""
    ssmSql = "SELECT DISTINCT aircraft_config_id,aircraft_code" \
             " FROM aircraft_config" \
             " WHERE aircraft_tail='%s'" \
             % (ssm.aircraft_tail)
    printlog(2, "%s" % ssmSql)
    cur = conn.cursor()
    cur.execute(ssmSql)

    aircraft_config_id = 0
    aircraft_code = None
    for row in cur:
        aircraft_config_id = row[0]
        aircraft_code = row[1]
        printlog(1, "Aircraft code %s" % aircraft_code)

    return aircraft_config_id, aircraft_code