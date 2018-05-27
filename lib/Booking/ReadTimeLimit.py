# @file ReadTimeLimit.py

import sys
import operator
import psycopg2
from BarsLog import set_verbose, get_verbose, printlog
from ReadDateTime import ReadDate


def ReadTimeLimit(conn, bno):

    printlog("Find time limit for booking %d" % bno, 2)
    bookSql = \
        "select remark_text,processing_flag,limit_date,queue_code,timelmt_type,limit_time_mns from book_time_limits where book_no=%d" \
            % bno
    printlog(bookSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(bookSql)
    ldates = []
    for row in cur:
        ldate = ReadDate(str(row['limit_date']))
        printlog("Time limit %s : %s %s" % (ldate, row['processing_flag'], row['remark_text']))
        ldates.append(ldate)
    cur.close()
    return ldates

