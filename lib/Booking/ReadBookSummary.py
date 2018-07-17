# @file ReadBookSummary.py
"""
Query as used in BookingSummary.ec

select
      bs.booking_number,
      bs.booking_date_time,
      (select b.origin_address from book as b
       where b.book_no = bs.booking_number) as origin_address,
      bs.booking_summary_type_rcd,
      bs.pax_name,
      bs.sid_no
from booking_summary as bs
sid_no is for NoFlySelecteePassengerId (not used)
"""

import sys
import operator
import psycopg2  # Informix DB module
from psycopg2 import extras
from BarsLog import blogger


def ReadBookSummary(conn, book_no, report_code=None):
    """Find booking summary.

    Check if there are any pending emails

    @param conn             database connection
    @param book_no          booking number
    @param report_code      message code

    @return number of entries found
    """
    blogger().debug("Find bookings summary"),
    bk_summ = \
        "SELECT booking_number,booking_summary_type_rcd,pax_name" \
        " FROM booking_summary" \
        " WHERE 1=1"
    if book_no is not None:
        blogger().debug("booking %d" % book_no),
        bk_summ += \
            " AND booking_number=%d" \
            % (book_no)
    if report_code is not None:
        blogger().debug("message type %s" % report_code),
        bk_summ += \
            " AND booking_summary_type_rcd='%s'" \
            % report_code
    blogger().debug(bk_summ)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bk_summ)
    n = 0
    for row in cur:
        print("Book summary %d %s : %s"
              % (int(row['booking_number'] or 0),
                 row['booking_summary_type_rcd'], row['pax_name']))
        n += 1

    return n


def ReadBookSummaryHistory(conn, book_no, hist_code=None, email_date=None):
    """
    Check if there are any pending emails

    @param conn             database connection
    @param book_no          booking number
    @param hist_code        message code
    @param email_date       cutoff date, usually 24 hours ago

    @return number of entries found
    """
    blogger().debug("Find bookings summary history")
    bk_summ = \
        "SELECT book_no,book_summary_history_rcd,sent_date_time" \
        " FROM book_summary_history" \
        " WHERE 1=1"
    if book_no is not None:
        blogger().debug("booking %d" % book_no)
        bk_summ += \
            " AND book_no=%d" \
            % (book_no)
    if hist_code is not None:
        blogger().debug("message type %s" % hist_code)
        bk_summ += \
            " AND book_summary_history_rcd='%s'" \
            % (hist_code)
    if email_date is not None:
        blogger().debug("after %s" % email_date.strftime("%Y-%m-%d %H:%M:%S"))
        bk_summ += \
            " AND sent_date_time>'%s'" \
            % email_date.strftime("%Y-%m-%d %H:%M:%S")
    blogger().debug(" ")
    blogger().debug(bk_summ)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bk_summ)
    n = 0
    book_summary_history_rcd = None
    for row in cur:
        book_summary_history_rcd = row['book_summary_history_rcd']
        print("Book summary history %d sent message %s on %s"
              % (int(row['book_no'] or 0), book_summary_history_rcd,
                 row['sent_date_time']))
        n += 1

    return n
