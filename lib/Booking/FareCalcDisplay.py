# @file FareCalcDisplay.py
"""
Calculate and display fares.
"""

import psycopg2
from psycopg2 import extras

from BarsLog import blogger
from Booking.PricingData import SellingConfig, PricingData, FarePricingData
from Booking.PaymentData import PaymentData


def ReadSellingConfig(conn, acompany_code):
    """Read selling classes."""
    rscSql = """SELECT selling_class, cabin_code,
                parent_sell_cls, ffp_fact_mult,display_priority
                FROM selling_conf
                WHERE company_code = '%s'""" \
             % acompany_code
    blogger().debug(rscSql)
    cur = conn.cursor()
    cur.execute(rscSql)
    sellconfigs = {}
    for row in cur:
        selling_class = row[0]
        cabin_code = row[1]
        parent_sell_cls = row[2]
        ffp_fact_mult = row[3]
        display_priority = row[4]
        sellconf = SellingConfig(acompany_code, selling_class,
                                 parent_sell_cls, cabin_code,
                                 ffp_fact_mult, display_priority)
        sellconfigs[selling_class] = sellconf

    return sellconfigs


def FareCalcDisplay(conn,
                    acompany_code,
                    acity_pair,
                    taxes,
                    flightDate,
                    areturn_date,
                    aselling_class,
                    aoneway_return_flag,
                    afare_category,
                    aauthority_level,
                    aTargetDate,
                    fare_factor=1.0):
    """Fare calculation."""
    blogger().info("Calculate fare for city pair %d date %s"
             % (acity_pair, flightDate))
    fcdSql = """
    SELECT fs.fare_basis_code,
            fs.city_pair, fs.valid_from_date,
            fs.valid_to_date, fs.fare_amount,
            fc.short_description, fc.oneway_return_flag,
            fc.byps_strt_auth_level, fc.byps_end_auth_level,
            fc.selling_class
    FROM fare_segments fs, fare_basis_codes fc
    WHERE fs.company_code = '%s'
    AND fs.active_flag = 'A'
    AND fs.city_pair = %d
    AND fs.valid_from_date <= '%s'
    AND fs.valid_to_date >= '%s'
    AND fc.company_code = fs.company_code
    AND fc.fare_basis_code = fs.fare_basis_code
    AND fc.selling_class = '%s'
    AND fc.oneway_return_flag = '%s'
    AND fc.fare_category = '%s'
    AND fc.acss_strt_auth_level <= %d
    AND fc.acss_end_auth_level >= %d
    AND ( ( fs.eff_from_date <= '%s' AND fs.eff_to_date >= '%s' )
       OR ( fs.eff_from_date IS NULL )
       OR ( fs.eff_to_date IS NULL ) )
    ORDER BY fs.company_code, fs.city_pair, fs.fare_amount, fs.fare_basis_code
    """ % (acompany_code,
           acity_pair,
           flightDate.strftime('%Y-%m-%d'), flightDate.strftime('%Y-%m-%d'),
           aselling_class,
           aoneway_return_flag,
           afare_category,
           aauthority_level, aauthority_level,
           aTargetDate.strftime('%Y-%m-%d'), aTargetDate.strftime('%Y-%m-%d'))
    blogger().debug("%s" % fcdSql)
    cur = conn.cursor()
    cur.execute(fcdSql)

    aircraft_code = ''
    pricings = []
    blogger().debug("Selected %d row(s)" % cur.rowcount)
    for row in cur:
        fare_basis_code = row[0]
        city_pair = row[1]
        valid_from_date = row[2]
        valid_to_date = row[3]
        fare_amount = float(row[4])
        short_description = row[5]
        oneway_return_flag = row[6]
        byps_strt_auth_level = row[7]
        byps_end_auth_level = row[8]
        selling_class = row[9]
        fare_amount *= fare_factor
        blogger().debug("Fare %s from %s to %s class %s: %f"
                 % (fare_basis_code, valid_from_date, valid_to_date,
                    selling_class, fare_amount))
        pricing = FarePricingData(fare_basis_code,
                                  city_pair,
                                  valid_from_date,
                                  valid_to_date,
                                  fare_amount,
                                  short_description,
                                  oneway_return_flag,
                                  byps_strt_auth_level,
                                  byps_end_auth_level,
                                  selling_class[0])
        pricings.append(pricing)

    return pricings


