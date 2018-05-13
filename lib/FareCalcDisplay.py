# @file FareCalcDisplay.py

import psycopg2
    
from BarsLog import printlog
from PricingData import PricingData

def FareCalcDisplay(conn, 
                    acompany_code, 
                    acity_pair_no, 
                    aflight_date, 
                    areturn_date, 
                    aselling_cls_code, 
                    aonw_return_ind, 
                    afare_category, 
                    aauthority_level, 
                    aTargetDate):
    
    fcdSql = \
    """
    SELECT fs.fare_code,
            fs.city_pair_no, fs.valid_from_date,
            fs.valid_to_date, fs.fare_value,
            fc.short_description, fc.onw_return_ind,
            fc.byps_strt_auth_lvl, fc.byps_end_auth_lvl,
            fc.selling_cls_code
    FROM fare_segm fs, fare_codes fc
    WHERE fs.company_code = '%s' 
    AND fs.active_flag = 'A'
    AND fs.city_pair_no = %d
    AND 
    (
        (
            fs.valid_from_date <= '%s'
            AND fs.valid_to_date >= '%s'
            AND fc.onw_return_ind = 'O'
        ) 
        OR
        (
            fs.valid_from_date <= '%s'
            AND fs.valid_to_date >= '%s'
            AND fc.onw_return_ind = 'R' 
        )
    ) 
    AND fc.company_code = fs.company_code 
    AND fc.fare_code = fs.fare_code 
    AND fc.selling_cls_code = '%s'
    AND fc.onw_return_ind = '%s'
    AND fc.fare_category = '%s'
    AND fc.acss_strt_auth_lvl <= %d 
    AND fc.acss_end_auth_lvl >= %d 
    AND 
    (
        (
            fs.eff_from_date <= '%s'
            AND fs.eff_to_date >= '%s'
        ) 
        OR 
        (
            fs.eff_from_date IS NULL
        ) 
        OR
        (
            fs.eff_to_date IS NULL
        )
    )
    ORDER BY fs.company_code, fs.city_pair_no, fs.fare_value, fs.fare_code
    """ % (
    acompany_code,
    acity_pair_no,
    aflight_date, aflight_date, aflight_date, aflight_date,
    aselling_cls_code, 
    aonw_return_ind, 
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
        city_pair_no =  row[1]
        valid_from_date = row[2]
        valid_to_date = row[3]
        fare_value = float(row[4])
        short_description = row[5]
        onw_return_ind = row[6]
        byps_strt_auth_lvl = row[7]
        byps_end_auth_lvl = row[8]
        selling_cls_code = row[9]
        printlog(2, "Fare %s from %s to %s: %f" % (fare_code, valid_from_date, valid_to_date, fare_value))
        pricing = PricingData(fare_code,
                                city_pair_no,
                                valid_from_date,
                                valid_to_date,
                                fare_value,
                                short_description,
                                onw_return_ind,
                                byps_strt_auth_lvl,
                                byps_end_auth_lvl,
                                selling_cls_code)
        pricings.append(pricing)
        
    return pricings

    