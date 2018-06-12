# @file FareCalcDisplay.py
"""
Calculate and display fares.
"""

import psycopg2

from BarsLog import printlog
from Booking.PricingData import PricingData, FarePricingData
from Booking.PaymentData import PaymentData


def FareCalcDisplay(conn,
                    acompany_code,
                    acity_pair,
                    aflight_date,
                    areturn_date,
                    aselling_class,
                    aonw_return_flag,
                    afare_category,
                    aauthority_level,
                    aTargetDate):
    """Fare calculation."""
    fcdSql = """
    SELECT fs.fare_code,
            fs.city_pair, fs.valid_from_date,
            fs.valid_to_date, fs.fare_value,
            fc.short_description, fc.onw_return_flag,
            fc.byps_strt_auth_level, fc.byps_end_auth_level,
            fc.selling_class
    FROM fare_segm fs, fare_codes fc
    WHERE fs.company_code = '%s'
    AND fs.active_flag = 'A'
    AND fs.city_pair = %d
    AND ( ( fs.valid_from_date <= '%s'
            AND fs.valid_to_date >= '%s'
            AND fc.onw_return_flag = 'O' )
       OR ( fs.valid_from_date <= '%s'
            AND fs.valid_to_date >= '%s'
            AND fc.onw_return_flag = 'R' ) )
    AND fc.company_code = fs.company_code
    AND fc.fare_code = fs.fare_code
    AND fc.selling_class = '%s'
    AND fc.onw_return_flag = '%s'
    AND fc.fare_category = '%s'
    AND fc.acss_strt_auth_level <= %d
    AND fc.acss_end_auth_level >= %d
    AND ( ( fs.eff_from_date <= '%s' AND fs.eff_to_date >= '%s' )
       OR ( fs.eff_from_date IS NULL )
       OR ( fs.eff_to_date IS NULL ) )
    ORDER BY fs.company_code, fs.city_pair, fs.fare_value, fs.fare_code
    """ % (
    acompany_code,
    acity_pair,
    aflight_date, aflight_date, aflight_date, aflight_date,
    aselling_class,
    aonw_return_flag,
    afare_category,
    aauthority_level, aauthority_level,
    aTargetDate, aTargetDate)
    printlog(2, "%s" % fcdSql)
    cur = conn.cursor()
    cur.execute(fcdSql)

    aircraft_code = ''
    pricings = []
    printlog(2, "Selected %d row(s)" % cur.rowcount)
    for row in cur:
        fare_code = row[0]
        city_pair = row[1]
        valid_from_date = row[2]
        valid_to_date = row[3]
        fare_value = float(row[4])
        short_description = row[5]
        onw_return_flag = row[6]
        byps_strt_auth_level = row[7]
        byps_end_auth_level = row[8]
        selling_class = row[9]
        printlog(2, "Fare %s from %s to %s: %f"
                 % (fare_code, valid_from_date, valid_to_date, fare_value))
        pricing = FarePricingData(fare_code,
                                  city_pair,
                                  valid_from_date,
                                  valid_to_date,
                                  fare_value,
                                  short_description,
                                  onw_return_flag,
                                  byps_strt_auth_level,
                                  byps_end_auth_level,
                                  selling_class
                                  )
        pricings.append(pricing)

    return pricings


def ReadPayments(conn, book_no):
    """Read payments for booking."""
    RpSql = """
        SELECT payment_form, payment_type, paid_curr_code, payment_amount,
        payment_date,
        document_no, payment_mode, pax_name, pax_code,
        contact_phone_no,
        paid_flag, pay_stat_flag,
        update_time
        FROM payments
        WHERE book_no = %d""" % book_no
    printlog(2, RpSql)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(RpSql)
    for row in cur:
        payRec = PaymentData(row['payment_form'], row['payment_type'],
                             row['paid_curr_code'], row['payment_amount'],
                             row['payment_date'],
                             row['document_no'], row['payment_mode'],
                             row['pax_name'], row['pax_code'],
                             row['paid_flag'], row['pay_stat_flag'],
                             row['update_time'])
        payRec.display()


