# @file ReadAircraftConfig.py


import sys
import psycopg2
from BarsLog import set_verbose, get_verbose, printlog
from ReadDateTime import ReadDate

# Read table aircraft_config
def ReadAircraftConfig(conn, aircraft_code, config_table_no,
                       selling_cls_code, seat_capacity=0):

    print "Aircraft configuration for",
    AcSql = \
        "SELECT gen_flag_invt,aircraft_code,limit_sale_lvl,scrutiny_flg," \
        "update_time,config_table_no,company_code,selling_cls_code," \
        "seat_capacity,user_name" \
        " FROM aircraft_config"
    if aircraft_code is not None and config_table_no is not None:
        print "aircraft code %s" % aircraft_code,
        print "config table %s" % config_table_no,
        AcSql += \
            " WHERE aircraft_code='%s' AND config_table_no='%s'" \
                % (aircraft_code, config_table_no)
    elif aircraft_code is not None:
        print "aircraft code %s" % aircraft_code,
        AcSql += \
            " WHERE aircraft_code='%s'" % aircraft_code
    elif config_table_no is not None:
        print "config table %s" % config_table_no,
        AcSql += \
            " WHERE config_table_no='%s'" % config_table_no
    if selling_cls_code is not None:
        print "class %s" % selling_cls_code,
        AcSql += \
            " AND selling_cls_code='%s'" % selling_cls_code
    if seat_capacity > 0:
        print "seat capacity %d" % seat_capacity,
        AcSql += \
            " AND seat_capacity=%d" % seat_capacity
    print "[aircraft_config]"
    printlog(AcSql, 1)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(AcSql)
    n = 0
    for row in cur:
        n += 1
        print "\tconfig table %5s aircraft code %4s capacity %3d class %s company %s inventory %s user %s update %s" \
            % (row['config_table_no'], row['aircraft_code'], row['seat_capacity'], row['selling_cls_code'],
               row['company_code'], row['gen_flag_invt'], row['user_name'], row['update_time'])

    if n == 0:
        print "\tnot found"

