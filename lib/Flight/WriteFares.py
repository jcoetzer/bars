# @file WriteFares.py
"""
Add and delete fare related data.
"""
import psycopg2

from BarsLog import printlog


def AddCityPair(conn, depart_airport, arrive_airport, aUser, aGroup):
    """New city pair."""
    printlog(1, "Add city pair depart %s arrive %s"
             % (depart_airport, arrive_airport))
    AcpSql = """
    INSERT INTO city_pair(
        departure_city, arrival_airport, pair_indicator, distance,
        baggage_alownce, pair_rule_no, remarks,
        update_user, update_group, update_time)
    VALUES(
        '%s', '%s', 1, 'A', %d,
        '20kg', 1, '',
        'SSM', 'BARS', NOW())
    RETURNING city_pair""" \
    % (depart_airport, arrive_airport, aUser, aGroup)

    printlog(2, "%s" % AcpSql)
    cur = conn.cursor()
    cur.execute(AcpSql)

    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    city_pair = 0
    for row in cur:
        city_pair = int(row[0])

    printlog(1, "New city pair %d" % city_pair)
    return city_pair


def AddFare(conn, company_code, fare_code, selling_class, aUser, aGroup):
    """New fare."""
    printlog(1, "Add fare %s class %s" % (fare_code, selling_class))
    AfSql = """
    INSERT INTO fare_codes(
        company_code, fare_code, short_description, description,
        selling_class, fare_category, onw_return_flag,
        acss_strt_auth_level, acss_end_auth_level,
        update_user, update_group, update_time)
    VALUES(
        '%s', '%s', 'Fare', 'Fare stuff',
        '%s', 'ZZOW', 'R', 100, 200, '%s', '%s', NOW() )""" \
    % (company_code, fare_code, selling_class, aUser, aGroup)

    printlog(2, "%s" % AfSql)
    cur = conn.cursor()
    cur.execute(AfSql)

    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def AddFares(conn, company_code, depart_airport, arrive_airport,
             selling_classes, aUser, aGroup):
    """New fares."""
    fare_code = 'X' + company_code + depart_airport + arrive_airport
    n = len(selling_classes)
    i = 0
    while i < n:
        AddFare(conn, company_code, fare_code, selling_classes[i],
                aUser, aGroup)
        i += 1


def DelFares(conn, company_code, depart_airport, arrive_airport):
    """New fares."""
    fare_code = 'X' + company_code + depart_airport + arrive_airport
    DfSql = """DELETE FROM fare_codes
    WHERE company_code='%s' AND fare_code='%s'""" \
    % (company_code, fare_code)

    printlog(2, "%s" % DfSql)
    cur = conn.cursor()
    cur.execute(DfSql)

    printlog(2, "Deleted %d row(s)" % cur.rowcount)


def AddFareSegment(conn, company_code, fare_code,
                   city_pair, depart_airport, arrive_airport, dt1, dt2,
                   fare_amount,
                   aUser, aGroup):
    """New fare segment."""
    printlog(1, "Add fare segment %s depart %s arrive %s value %d"
             % (fare_code, depart_airport, arrive_airport, fare_amount))
    AfsSql = """
    INSERT INTO fare_segm(
        company_code, fare_code, city_pair, valid_from_date, valid_to_date,
        fare_amount, active_flag,
        update_user, update_group, update_time )
    VALUES (
        '%s', '%s', %d, '%s', '%s',
        %d.0, 'A',
        '%s', '%s', NOW() )""" \
    % (company_code, fare_code, city_pair, dt1, dt2,
       fare_amount, aUser, aGroup)

    printlog(2, "%s" % AfsSql)
    cur = conn.cursor()
    cur.execute(AfsSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def AddFareSegments(conn, company_code, depart_airport, arrive_airport,
                    city_pair, dt1, dt2, fare_amount,
                    aUser, aGroup):
    """New fare segments."""
    fare_code = 'X' + company_code + depart_airport + arrive_airport
    AddFareSegment(conn, company_code, fare_code,
                   city_pair, depart_airport, arrive_airport, dt1, dt2,
                   fare_amount, aUser, aGroup)


def DelFareSegments(conn, company_code, depart_airport, arrive_airport,
                    dt1, dt2):
    """New fares."""
    fare_code = 'X' + company_code + depart_airport + arrive_airport
    printlog(1, "Delete fare segment %s depart %s arrive %s"
             % (fare_code, depart_airport, arrive_airport))
    DfSql = """DELETE FROM fare_segm
    WHERE company_code='%s' AND fare_code='%s'
    AND valid_from_date='%s' AND valid_to_date='%s'""" \
    % (company_code, fare_code, dt1, dt2)

    printlog(2, "%s" % DfSql)
    cur = conn.cursor()
    cur.execute(DfSql)

    printlog(2, "Deleted %d row(s)" % cur.rowcount)
