# @file ReadFlightSegments.py

import os
import sys
import psycopg2
import time
from datetime import datetime, timedelta, date
from FlightData import FlightData
from BarsLog import printlog, get_verbose
from ReadDateTime import ReadDate


def ReadSegmentStatus(conn, flight_number, flight_date):

    print "Segment status for flight %s board date %s [segment_status]" \
        % (flight_number, flight_date.strftime("%Y-%m-%d"))
    RcSql = \
        "select city_pair_no,selling_cls_code,status_type,segm_status_code,leg_status_code,processing_flg" \
        " from segment_status" \
        " WHERE flight_number='%s'" \
        " AND flight_date='%s'" \
            % (flight_number, flight_date.strftime("%m/%d/%Y"))
    printlog(RcSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cur.execute("set isolation dirty read")
    cur.execute(RcSql)
    for row in cur:
        print "\tcity pair %3d class %s status type %s status code %s processed %s" \
            % (row['city_pair_no'], row['selling_cls_code'], row['status_type'], row['segm_status_code'], row['processing_flg'])
