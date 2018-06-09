"""
Red data from booking tables.

@file ReadBooking.py
"""

import os
import sys
import operator
import psycopg2

from datetime import datetime, timedelta, date

from BarsLog import set_verbose, get_verbose, printlog
# from ReadBookings import GetBookColumns


def ReadBooking(conn, book_no):
    dt1 = None
    bcol = "booking_status,pax_name_rec,origin_address,first_segm_date," \
           "no_of_seats,book_agency"
    # GetBookColumns()

    bookSql = \
        "SELECT %s FROM book WHERE book_no=%d" % (bcol, book_no)

    print("Booking %d" % book_no)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(bookSql)
    for row in cur:
        pnr = row['pax_name_rec']
        dt1 = row['first_segm_date']
        print("\t%s %s %s %s %s %s"
              % (row['booking_status'], row['pax_name_rec'],
                 row['origin_address'], row['first_segm_date'],
                 row['no_of_seats'], row['book_agency']))

    cur.close()
    return pnr, dt1


def ReadBookingData(conn, bk_cfg_files, book_no, locator):

    for bk_cfg_file in bk_cfg_files:

        printlog(2, "Read config file %s" % bk_cfg_file)
        f = open(bk_cfg_file, "r")

        fnames = os.path.basename(bk_cfg_file).split('.')

        fname = fnames[1]

        lines = f.readlines()

        f.close()

        for line in lines:
            if line[0] == '#':
                continue
            fields = line.split(';')
            tabname = fields[0]
            colnames = fields[1].strip()
            if fname == 'book_no':
                bookSql = "SELECT %s FROM %s where book_no=%d" \
                    % (colnames, tabname, book_no)
            elif fname == 'booking_no':
                bookSql = "SELECT %s FROM %s where booking_no=%d" \
                    % (colnames, tabname, book_no)
            elif fname == 'locator':
                bookSql = "SELECT %s FROM %s where locator='%s'" \
                    % (colnames, tabname, locator)
            elif fname == 'book_no':
                bookSql = "SELECT %s FROM %s where book_no=%d" \
                    % (colnames, tabname, book_no)
            else:
                print("Unknown field [%s]" % fname)
                return
            print("%s:" % tabname)
            printlog(2, "%s" % bookSql)

            cur = conn.cursor()
            # Run query
            cur.execute(bookSql)
            rows = cur.fetchall()
            cur.close()
            colwids = []
            for row in rows:
                n = 0
                for i in range(len(row)):
                    colwids.append(0)
                for col in row:
                    lc = len(str(col or ''))
                    if n == 0:
                        colwids[n] = lc
                    elif lc > colwids[n]:
                        colwids[n] = lc
                    else:
                        pass
                    n += 1
            for row in rows:
                n = 0
                for col in row:
                    print("%-*s" % (colwids[n], str(col or '')), end=' ')
                    n += 1
                print('')
            print('')

    cur.close()
