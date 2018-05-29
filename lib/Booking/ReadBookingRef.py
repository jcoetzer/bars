# @file ReadBookingRef.py

import sys
import operator
import psycopg2

from BarsLog import printlog

def ReadBookNo(conn, bno):

    if bno is None:
        return None
    locator = None
    bookSql = \
        "SELECT pax_name_rec" \
        " FROM book WHERE book_no=%d" % bno
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bookSql)
    for row in cur:
        locator = str(row['pax_name_rec'] or '')
    cur.close()
    return locator


def ReadLocator(conn, locator):

    if locator is None:
        return None
    bno = int(0)
    bookSql = \
        "SELECT b.book_no bookno" \
        " FROM book b WHERE pax_name_rec='%s'" % locator
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bookSql)
    for row in cur:
        bno = int(row['bookno'])
    cur.close()
    return bno


def ReadBookSummaryHistory(conn, bno, bs_date=None):

    bookSql = \
        "SELECT book_summary_history_rcd, sent_date_time FROM book_summary_history WHERE book_no=%d" \
            % bno
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bookSql)
    rcd = ''
    sdt = ''
    for row in cur:
        rcd = row['book_summary_history_rcd']
        sdt = row['sent_date_time']
        printlog("Booking %d summary history received %s on %s" % (bno, rcd, sdt), 1)
    cur.close()
    return rcd, sdt


def ReadBookSummary(conn, bno):

    bookSql = \
        "SELECT booking_summary_type_rcd FROM booking_summary WHERE booking_number=%d" \
            % bno
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bookSql)
    rcd = ''
    for row in cur:
        rcd = row['booking_summary_type_rcd']
        printlog("Booking %d summary received %s" % (bno, rcd), 1)
    cur.close()
    return rcd
