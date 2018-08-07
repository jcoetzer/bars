# @file ReadTaxes.py
"""
Read taxes.
"""

import psycopg2
from psycopg2 import extras


from datetime import datetime, date

class TaxData(object):

    def __init__(self, company_code, tax_code, pax_code, tax_sequence,
                 tax_type, tax_amount, nuc_rate,
            valid_from_date, valid_to_date,
            short_description):
        self.company_code = company_code
        self.tax_code = tax_code
        self.pax_code = pax_code
        self.tax_sequence = int(tax_sequence)
        self.tax_type = tax_type
        self.tax_amount = float(tax_amount)
        self.nuc_rate = nuc_rate
        self.valid_from_date = valid_from_date
        self.valid_to_date = valid_to_date
        self.short_description = short_description

    def __lt__(self,other):
         return self.tax_sequence > other.tax_sequence

    def display(self):
        print("Tax %3d %s start %s end %s %s %f : %s"
              % (self.tax_sequence, self.tax_code,
                 self.valid_from_date, self.valid_to_date,
                 self.tax_type, self.tax_amount, self.short_description))


def ApplyTaxes(conn, aBaseFare, aTaxes):
    rval = float(aBaseFare)
    for tax in aTaxes:
        if tax.tax_type == '=':
            rval += tax.tax_amount
        elif tax.tax_type == '%':
            rval *= 1 + (self.tax_amount / 100)
        else:
            pass
    return rval


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
            AND ( ( valid_from_date <= '%s' AND valid_to_date >= '%s' AND '%s' IN ( 'O', 'B', ' ' ) )
                  OR ( valid_from_date <= '%s' AND valid_to_date >= '%s' AND '%s' = 'R'
                     AND ( ( valid_from_date <= '%s' AND valid_to_date >= '%s' AND '%s' != '' ) OR '%s' = '' ) ) )""" \
    % (aCompanyCode, pass_code1, pass_code2,
       aAirport,
       aState,
       aNation,
       flightDate, returnDate, aReturnInd,
       flightDate, returnDate, aReturnInd,
       flightDate, returnDate, returnDate, returnDate)
    logger.debug("%s" % RtSql)
    cur = conn.cursor()
    cur.execute(RtSql)

    taxes = []
    logger.debug("Selected %d row(s)" % cur.rowcount)
    for row in cur:
        tax = TaxData(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                      row[7], row[8], row[9])
        #tax.display()
        taxes.append(tax)
        #for item in row:
            #print("%s" % item),
        #print('')

    cur.close()
    taxes.sort()
    return taxes


