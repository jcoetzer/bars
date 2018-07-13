"""
Read payments.

@file ReadPayments.py
"""

import psycopg2
from psycopg2 import extras

from BarsLog import blogger
from Booking.PaymentData import PaymentData


def ReadPayments(conn, book_no):
    """Read payments for booking."""
    blogger.info("Read payments for booking %d" % book_no)
    RpSql = """
        SELECT payment_form, payment_type, currency_code, payment_amount,
        payment_date,
        document_no, payment_mode, pax_name, pax_code,
        contact_phone_no,
        paid_flag, pay_stat_flag,
        update_time
        FROM payments
        WHERE book_no = %d""" % book_no
    blogger.debug(RpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RpSql)
    for row in cur:
        payRec = PaymentData(row['payment_form'], row['payment_type'],
                             row['currency_code'], row['payment_amount'],
                             row['payment_date'],
                             row['document_no'], row['payment_mode'],
                             row['pax_name'], row['pax_code'],
                             row['paid_flag'], row['pay_stat_flag'],
                             row['update_time'])
        payRec.display()


def GetPriceSsr(conn, ssr_code):
    """Get price e.a. for SSR."""
    gpsSql = """SELECT fee_type_rcd, fee_code, description,
             fee_currency, fee_amount,
             payment_type, payment_form
             FROM fees
             WHERE ssr_code = '%s'""" % ssr_code
    blogger.debug(gpsSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(gpsSql)
    famount = 0.0
    fcurr = ''
    fcode = ''
    for row in cur:
        blogger.info("SSR %s : fee %s %s%f : %s"
                 % (ssr_code, row['fee_code'], row['fee_currency'],
                    row['fee_amount'], row['description']))
        famount = float(row['fee_amount'])
        fcurr = str(row['fee_currency'])
        fcode = str(row['fee_code'])
    blogger.info("Price for SSR %s : %s%.2f" % (ssr_code, fcurr, famount))
    return fcode, fcurr, famount
