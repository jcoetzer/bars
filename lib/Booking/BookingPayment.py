"""
Booking payment stuff.

@file BookingPayment.py
"""
import psycopg2

from BarsLog import printlog


def BookingIsPaid(conn, pbook_no, vbookstatus=None):
    '''
    Check booking paid status

    @param conn             database connection
    @param pbook_no         booking number
    @param vbookstatus      booking status

    @return True when booking is paid
    '''

    vfaresum = 0
    vfeesum = 0
    vpaymsum = 0
    cBookNo = None

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query

    if vbookstatus is None:
        # Check if booking cancelled
        bk_cnl="SELECT booking_status, book_no FROM book WHERE book_no=%d" % pbook_no
        printlog(bk_cnl, 2)
        cur.execute(bk_cnl)
        for row in cur:
            vbookstatus = row['booking_status']

    if pbook_no is not None:
        # Check if book_no is valid
        if vbookstatus is not None and vbookstatus=='X' :
            printlog("Booking %d was cancelled" % pbook_no,1)
            return False

        # Sum up payments
        vpaymsum = float(0.0)
        bk_pay="SELECT sum(payment_amount) vpaymsum FROM payments WHERE book_no=%d AND payment_type not in ('BC','BT','WF') AND paid_flag='Y'" % pbook_no
        printlog(bk_pay, 2)
        cur.execute(bk_pay)
        for row in cur:
            vpaymsum = float(row['vpaymsum'] or 0.0)

        # Sum up fares, taxes and surcharges
        vfaresum = float(0.0)
        bk_fares="SELECT sum(fare_paymt_amt) vfaresum FROM book_fares_paym p,passenger pas WHERE p.book_no=%d AND pas.book_no=p.book_no AND pas.pass_code=p.pass_code" % pbook_no
        printlog(bk_fares, 2)
        cur.execute(bk_fares)
        for row in cur:
            vfaresum = float(row['vfaresum'] or 0.0)

        # Sum up fees
        vfeesum = float(0.0)
        bk_fees="SELECT sum(payment_amount) vfeesum FROM payments WHERE book_no=%d AND payment_type in ('BC','BT','WF')" % pbook_no
        printlog(bk_fees, 2)
        cur.execute(bk_fees)
        for row in cur:
            vfeesum = float(row['vfeesum'] or 0.0)

        paychk = round((vpaymsum + vfeesum) - vfaresum,2)
        if vpaymsum == 0.0:
            printlog("Booking %d payment %.2f fares %.2f fees %.2f unpaid (%f)" % (pbook_no, vpaymsum, vfaresum, vfeesum, paychk), 1)
            retstring=False
        elif paychk>=0.0 :
            printlog("Booking %d payment %.2f fares %.2f fees %.2f paid (%f)" % (pbook_no, vpaymsum, vfaresum, vfeesum, paychk), 1)
            retstring=True
        else:
            printlog("Booking %d payment %.2f fares %.2f fees %.2f not fully paid (check %f)" % (pbook_no, vpaymsum, vfaresum, vfeesum, paychk), 1)
            retstring=False
    else:
        print "Booking number not supplied"
        retstring=False

    cur.close()

    return retstring