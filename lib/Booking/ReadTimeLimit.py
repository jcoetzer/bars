# @file ReadTimeLimit.py
"""
Find time limit for booking.
"""

import sys
import operator
import psycopg2
import logging
from psycopg2 import extras
from BarsLog import blogger
from ReadDateTime import ReadDate


def ReadTimeLimit(conn, bno):

    blogger.debug("Find time limit for booking %d" % bno)
    bookSql = \
        "select remark_text,processing_flag,limit_date,queue_code," \
        "timelmt_type,limit_time_mns from book_time_limits where book_no=%d" \
        % bno
    blogger.debug(bookSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(bookSql)
    ldates = []
    for row in cur:
        ldate = ReadDate(str(row['limit_date']))
        blogger.info("Time limit %s : %s %s"
                 % (ldate, row['processing_flag'], row['remark_text']))
        ldates.append(ldate)
    cur.close()
    return ldates

