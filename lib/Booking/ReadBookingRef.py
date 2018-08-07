"""
Read booking references.

@file ReadBookingRef.py
"""

import sys
import operator
import logging
import psycopg2
from psycopg2 import extras


logger = logging.getLogger("web2py.app.bars")


def ReadBookNo(conn, bno):
    """Read booking number."""
    if bno is None:
        return None
    locator = None
    bookSql = \
        "SELECT locator" \
        " FROM bookings WHERE book_no=%d" % bno
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bookSql)
    for row in cur:
        locator = str(row['locator'] or '')
    cur.close()
    return locator


def ReadLocator(conn, locator):
    """Read locator."""
    if locator is None:
        return None
    bno = int(0)
    bookSql = \
        "SELECT b.book_no bookno" \
        " FROM bookings b WHERE locator='%s'" % locator
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bookSql)
    for row in cur:
        bno = int(row['bookno'])
    cur.close()
    return bno


def ReadBookSummaryHistory(conn, bno, bs_date=None):
    """Read booking summary history."""
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
        logger.info("Booking %d summary history received %s on %s"
                     % (bno, rcd, sdt))
    cur.close()
    return rcd, sdt


def ReadBookSummary(conn, bno):
    """Read booking summary."""
    bookSql = \
        "SELECT booking_summary_type_rcd FROM booking_summary WHERE booking_number=%d" \
            % bno
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bookSql)
    rcd = ''
    for row in cur:
        rcd = row['booking_summary_type_rcd']
        logger.info("Booking %d summary received %s" % (bno, rcd), 1)
    cur.close()
    return rcd

