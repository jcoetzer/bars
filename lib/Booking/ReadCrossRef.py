# @file ReadCrossRef.py
#

import os
import sys
import getopt
import psycopg2
from datetime import datetime, timedelta, date

def check_bci_new(conn, ExtOriginAddress, ExtBookNumb, PnrBookNumb, msk):
    print "Check booking cross index for origin %s external %s locator %s :" \
        % (ExtOriginAddress, ExtBookNumb, PnrBookNumb)
    ChkSql = \
        "SELECT bci.book_no bno, bci.ext_book_numb ext, bci.pax_name_rec pnr, bci.book_category bcat, bci.origin_address bor" \
        " FROM book_crs_index bci \n" \
        " WHERE \n(\n  1=0\n"
    if msk & 1:
        ChkSql += \
            "  OR ( 1=1 AND len(bci.ext_book_numb) > 2" \
            " AND bci.origin_address = '%s'" \
            " AND bci.ext_book_numb = '%s')\n" \
                % (ExtOriginAddress, ExtBookNumb)
    if msk & 2:
        ChkSql += \
            "  OR ( 2=2 AND bci.ext_book_numb IS NULL" \
            " AND bci.pax_name_rec = '%s' AND len(bci.pax_name_rec) > 2 ) \n" \
                % PnrBookNumb
    if msk & 4:
        ChkSql += \
            "  OR ( 3=3 AND len(bci.pax_name_rec)>2" \
            " AND bci.ext_book_numb != '%s'" \
            " AND bci.origin_address != '%s'\n" \
            "       AND bci.pax_name_rec = (SELECT b.pax_name_rec FROM book b, book_crs_index bc" \
            " WHERE bc.book_no=b.book_no AND bc.ext_book_numb = '%s'" \
            " AND bc.origin_address != '%s' ) ) \n" \
                % (ExtBookNumb, ExtOriginAddress, ExtBookNumb, ExtOriginAddress)
    if msk & 8:
        ChkSql += \
            "  OR ( 4=4 AND len(bci.pax_name_rec) > 2" \
            " AND bci.pax_name_rec != ''" \
            " AND bci.ext_book_numb = '%s'" \
            " AND bci.origin_address = '%s'" \
            " AND (bci.origin_address LIKE '%%1G' OR bci.origin_address LIKE '%%1P') )\n" \
                % (ExtBookNumb, ExtOriginAddress)
    ChkSql += \
        ") "
    printlog("%s" % ChkSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ChkSql)
    for row in cur:
        print "\tbook %s origin %s ext %s locator %s category %s" \
            % (row['bno'], row['bor'], row['ext'], row['pnr'], row['bcat'])


def check_bci_trl(conn, ExtOriginAddress, ExtBookNumb, PnrBookNumb):
    print "Check booking cross index for origin %s external %s locator %s :" \
        % (ExtOriginAddress, ExtBookNumb, PnrBookNumb)

    ChkSql = \
        "SELECT bci.book_no bno, bci.ext_book_numb ext, b.pax_name_rec pnr, b.book_category bcat, b.no_of_seats n" \
        " FROM book_crs_index bci, book b " \
        " WHERE ( ( bci.ext_book_numb IS NOT NULL " \
        "          AND bci.origin_address = \"%s\" " \
        "          AND bci.ext_book_numb = \"%s\" ) OR " \
        "        ( bci.ext_book_numb IS NULL " \
        "          AND bci.pax_name_rec = \"%s\" ) ) " \
        " AND bci.book_no = b.book_no" \
            % (ExtOriginAddress, ExtBookNumb, PnrBookNumb)
    printlog("%s" % ChkSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ChkSql)
    for row in cur:
        print "\tbook %s ext %s pnr %s category %s (%d seats)" \
            % (row['bno'], row['ext'], row['pnr'], row['bcat'], row['n'])


def check_bci(conn, ExtOriginAddress, ExtBookNumb, PnrBookNumb, msk):
    print "Check booking cross index for origin %s external %s locator %s :" \
        % (ExtOriginAddress, ExtBookNumb, PnrBookNumb)
    ChkSql = \
        "SELECT bci.book_no bno, bci.ext_book_numb ext, bci.pax_name_rec pnr, bci.book_category bcat" \
        " FROM book_crs_index bci\n" \
        " WHERE (\n  1=0\n"
    if msk & 1:
        ChkSql += \
            "  OR ( bci.ext_book_numb IS NOT NULL" \
            " AND bci.origin_address = '%s'" \
            " AND bci.ext_book_numb = '%s' )\n" \
                % (ExtOriginAddress, ExtBookNumb)
    if msk & 2:
        ChkSql += \
            "  OR ( bci.ext_book_numb IS NULL" \
            "          AND bci.pax_name_rec = '%s' AND len(bci.pax_name_rec) > 2 ) \n" \
                % PnrBookNumb
    if msk & 4:
        ChkSql += \
            "  OR ( bci.pax_name_rec IS NOT NULL" \
            " AND bci.ext_book_numb != '%s'" \
            " AND bci.origin_address != '%s'\n" \
            "       AND bci.pax_name_rec = (SELECT b.pax_name_rec FROM book b, book_crs_index bc" \
            " WHERE bc.book_no=b.book_no AND bc.ext_book_numb = '%s'" \
            " AND bc.origin_address != '%s' ) ) \n" \
                % (ExtBookNumb, ExtOriginAddress, ExtBookNumb, ExtOriginAddress)
    if msk & 8:
        ChkSql += \
            "  OR ( bci.pax_name_rec IS NOT NULL" \
            " AND bci.ext_book_numb = '%s'" \
            " AND bci.origin_address != '%s'" \
            " AND (bci.origin_address LIKE '%%1G' OR bci.origin_address LIKE '%%1P'))\n" \
                % (ExtBookNumb, ExtOriginAddress)
    ChkSql += \
        ")"
    printlog("%s" % ChkSql, 2)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ChkSql)
    for row in cur:
        print "\tbook %s ext %s pnr %s category %s" \
            % (row['bno'], row['ext'], row['pnr'], row['bcat'])
