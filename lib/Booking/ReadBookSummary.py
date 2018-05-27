# @file ReadBookSummary.py

import sys
import operator
import psycopg2  # Informix DB module
from BarsLog import set_verbose, get_verbose, printlog

# Query used in BookingSummary.ec:
#
# select
#       bs.booking_number,
#       bs.booking_date_time,
#       (select b.origin_address from book as b where b.book_no = bs.booking_number) as origin_address,
#       bs.booking_summary_type_rcd,
#       bs.passenger_name,
#       bs.sid_no
# from booking_summary as bs
# sid_no is for NoFlySelecteePassengerId (not used)

'''
Check if there are any pending emails

@param conn             database connection
@param book_no          booking number
@param report_code      message code

@return number of entries found
'''
def ReadBookSummary(conn, book_no, report_code=None):

    if get_verbose() >= 2: print "Find book summary",
    bk_summ = \
        "SELECT booking_number,booking_summary_type_rcd,passenger_name" \
        " FROM booking_summary" \
        " WHERE 1=1"
    if book_no is not None:
        if get_verbose() >= 2: print "booking %d" % book_no,
        bk_summ += \
            " AND booking_number=%d" \
            % (book_no)
    if report_code is not None:
        if get_verbose() >= 2: print "message type %s" % report_code,
        bk_summ += \
            " AND booking_summary_type_rcd='%s'" \
                % report_code
    if get_verbose() >= 2: print
    printlog(bk_summ, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bk_summ)
    n = 0
    for row in cur:
        print "Book summary %d %s : %s" % (int(row['booking_number'] or 0), row['booking_summary_type_rcd'], row['passenger_name'])
        n += 1

    return n


'''
Check if there are any pending emails

@param conn             database connection
@param book_no          booking number
@param hist_code        message code
@param email_date       cutoff date, usually 24 hours ago

@return number of entries found
'''
def ReadBookSummaryHistory(conn, book_no, hist_code=None, email_date=None):

    if get_verbose() >= 2: print "Find book summary history",
    bk_summ = \
        "SELECT book_no,book_summary_history_rcd,sent_date_time FROM book_summary_history" \
        " WHERE 1=1"
    if book_no is not None:
        if get_verbose() >= 2: print "booking %d" % book_no,
        bk_summ += \
            " AND book_no=%d" \
                % (book_no)
    if hist_code is not None:
        if get_verbose() >= 2: print "message type %s" % hist_code,
        bk_summ += \
            " AND book_summary_history_rcd='%s'" \
                % (hist_code)
    if email_date is not None:
        if get_verbose() >= 2: print "after %s" % email_date.strftime("%Y-%m-%d %H:%M:%S")
        bk_summ += \
            " AND sent_date_time>'%s'" \
                % email_date.strftime("%Y-%m-%d %H:%M:%S")
    if get_verbose() >= 2: print
    printlog(bk_summ, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bk_summ)
    n = 0
    book_summary_history_rcd = None
    for row in cur:
        book_summary_history_rcd = row['book_summary_history_rcd']
        #printlog("Book summary history %d sent message %s on %s" % (int(row['book_no'] or 0), book_summary_history_rcd, row['sent_date_time']))
        print "Book summary history %d sent message %s on %s" % (int(row['book_no'] or 0), book_summary_history_rcd, row['sent_date_time'])
        n += 1

    return n
