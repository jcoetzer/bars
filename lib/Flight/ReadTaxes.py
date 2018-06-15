# @file ReadTaxes.py
"""
Read taxes.
"""

import psycopg2

from BarsLog import printlog
from datetime import datetime, date

def ReadTaxes(conn, aCompanyCode, aFlightDate, aReturnDate, aAirport,
              pass_code1, pass_code2,
              aState, aNation,
              aReturnInd):
    """Read taxes for flight."""
    if aReturnDate is None:
        aReturnDate = aFlightDate
    flightDate = aFlightDate.strftime('%Y-%m-%d')
    returnDate = aReturnDate.strftime('%Y-%m-%d')
    RtSql = """SELECT company_code, tax_code,
            pax_code, tax_sequence, tax_type, tax_amount, nuc_rate,
            valid_from_date, valid_to_date,
            short_description
            FROM taxes, currency_codes
            WHERE company_code = '%s'
            AND pax_code IN ( '%s', '%s' )
            AND currency_code = tax_currency
            AND tax_category IN ('T')
            AND ( departure_airport IS NULL OR departure_airport = '%s' )
            AND ( state_code IS NULL OR state_code = '%s' )
            AND ( nation_code IS NULL OR nation_code = '%s' )
            AND (
                    ( valid_from_date <= '%s' AND valid_to_date >= '%s' AND '%s' IN ( 'O', 'B', ' ' ) )
                    OR
                    ( valid_from_date <= '%s' AND valid_to_date >= '%s' AND '%s' = 'R'
                      AND (  ( valid_from_date <= '%s' AND valid_to_date >= '%s' AND '%s' != '' )
                            OR '%s' = ''
                        )
                    )
                )""" \
    % (aCompanyCode, pass_code1, pass_code2,
       aAirport,
       aState,
       aNation,
       flightDate, returnDate, aReturnInd,
       flightDate, returnDate, aReturnInd,
       flightDate, returnDate, returnDate, returnDate)
    printlog(2, "%s" % RtSql)
    cur = conn.cursor()
    cur.execute(RtSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    for row in cur:
        for item in row:
            printlog(1, "%s" % item, end=' ')
        print

    cur.close()

