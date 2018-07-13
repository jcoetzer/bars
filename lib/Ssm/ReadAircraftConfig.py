# @file ReadAircraftConfig.py

import sys
import psycopg2
from psycopg2 import extras
from BarsLog import blogger
from ReadDateTime import ReadDate
from Ssm.AircraftData import AircraftData


def ReadAircraftConfig(conn, aircraft_code, config_table,
                       selling_class, seat_capacity=0):
    """Read table aircraft_config."""
    print("Aircraft configuration for", end=' ')
    AcSql = \
        "SELECT gen_flag_invt,aircraft_code,limit_sale_level,scrutiny_flag," \
        "update_time,config_table,company_code,selling_class," \
        "seat_capacity,update_user" \
        " FROM aircraft_config"
    if aircraft_code is not None and config_table is not None:
        print("aircraft code %s" % aircraft_code, end=' ')
        print("config table %s" % config_table, end=' ')
        AcSql += \
            " WHERE aircraft_code='%s' AND config_table='%s'" \
            % (aircraft_code, config_table)
    elif aircraft_code is not None:
        print("aircraft code %s" % aircraft_code, end=' ')
        AcSql += \
            " WHERE aircraft_code='%s'" % aircraft_code
    elif config_table is not None:
        print("config table %s" % config_table, end=' ')
        AcSql += \
            " WHERE config_table='%s'" % config_table
    if selling_class is not None:
        print("class %s" % selling_class, end=' ')
        AcSql += \
            " AND selling_class='%s'" % selling_class
    if seat_capacity > 0:
        print("seat capacity %d" % seat_capacity, end=' ')
        AcSql += \
            " AND seat_capacity=%d" % seat_capacity
    print("[aircraft_config]")
    blogger.debug(AcSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(AcSql)
    n = 0
    for row in cur:
        n += 1
        print("\tconfig table %5s aircraft code %4s capacity %3d class %s"
              " company %s inventory %s user %s update %s"
              % (row['config_table'], row['aircraft_code'],
                 row['seat_capacity'], row['selling_class'],
                 row['company_code'], row['gen_flag_invt'],
                 row['update_user'],
                 row['update_time'].strftime("%Y-%m-%d %H:%M")))

    if n == 0:
        print("\tnot found")
    cur.close()


def WriteEquipmentConfig(conn, companyCode, aircraftCode, configTable,
                         tailNumber, cabinClasses, seatCapacities,
                         updateUser, updateGroup):
    """Write equipment configuration)."""
    cur = conn.cursor()
    n = 0
    for cabinClass in cabinClasses:
        WecSql = """
            INSERT INTO equipment_config (
                company_code, aircraft_code, config_table, tail_number,
                cabin_code, seat_capacity,
                update_user, update_group, update_time )
            VALUES (
                '%s', '%s', '%s', '%s',
                '%s', '%s',
                '%s', '%s', NOW() )""" \
            % (companyCode, aircraftCode, configTable, tailNumber, cabinClass,
               seatCapacities[n],  updateUser, updateGroup)
        blogger.debug(WecSql)
        cur.execute(WecSql)
        n += 1
    cur.close()


def ReadEquipmentConfig(conn, tailNumber):
    """Read equipment configuration)."""
    RecSql = """
        SELECT company_code, aircraft_code, config_table, tail_number,
            cabin_code, seat_capacity
        FROM equipment_config
        WHERE tail_number = '%s'""" % tailNumber
    blogger.debug(RecSql)
    cur = conn.cursor()
    cur.execute(RecSql)

    if cur.rowcount == 0:
        return None

    cabinClasses = []
    seatCapacities = []
    for row in cur:
        companyCode = row[0]
        aircraftCode = row[1]
        configTable = row[2]
        tailNumber = row[3]
        cabinClasses.append(row[4])
        seatCapacities.append(row[5])

    if len(cabinClasses) == 0:
        blogger.debug("Equipment %s not found" % tailNumber)
        return None

    eqt = AircraftData(companyCode, aircraftCode, configTable,
                       tailNumber, cabinClasses, seatCapacities)
    return eqt
