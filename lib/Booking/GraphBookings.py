# @file GraphBookings.py

import sys
import operator
import time
import psycopg2  # Informix DB module
from datetime import datetime, timedelta, date
from BarsLog import set_verbose, get_verbose, printlog

def PrintScale(WIDTH):
    #echo "      0         10        20        30        40        50        60        70        80"
    P=0
    Q=int(WIDTH/10)
    sys.stdout.write("      0 ")
    while P < Q:
        P+=1
        sys.stdout.write("        %2d" % (P*10))
    sys.stdout.write("\n")

def PrintAxis(WIDTH):
    #echo "      0         10        20        30        40        50        60        70        80"
    P=0
    Q=int(WIDTH/10)
    sys.stdout.write("      +")
    while P < Q:
        P+=1
        sys.stdout.write("----+----|")
    sys.stdout.write("\n")


def PrintGraph(bookings, dt1, dt2, ORIGIN, WIDTH):

    sys.stderr.write("\x1b[2J\x1b[H")

    if ORIGIN is not None:
        print "Bookings from %s" % (ORIGIN),
    else:
        print "Bookings",
    print "between %s and %s" % (dt1.strftime("%Y-%m-%d %H:%M:00"), dt2.strftime("%Y-%m-%d %H:%M:59"))
    print

    PrintScale(WIDTH)
    PrintAxis(WIDTH)
    n=0
    ntotal=0

    while dt2 >= dt1:
        btime = dt2.strftime("%Y%m%d%H%M")
        try:
            nbookings=int(bookings[btime])
        except KeyError:
            nbookings=0
        n+=1
        ntotal+=nbookings
        stime = "%s:%s" % (btime[8:10], btime[10:12])
        if nbookings > WIDTH:
            print "%s |%s[%d]" % (stime, "*"*WIDTH,nbookings )
        else:
            print "%s |%s" % (stime, "*"*nbookings)
        dt2 -= timedelta(minutes=1)

    PrintAxis(WIDTH)
    PrintScale(WIDTH)
    Avg=float(ntotal/n)
    print "\nTotal   : %d\t" % ntotal,
    print "Average : %.1f/min\n" % Avg


def InitGraphBookings(conn, dt1, dt2, ORIGIN=None, WIDTH=0):

    SQL = "SELECT update_time FROM book"
    SQL += " WHERE update_time>'%s' " % dt1.strftime("%Y/%m/%d/%H/%M/00")
    SQL += " AND update_time<'%s' " % dt2.strftime("%Y/%m/%d/%H/%M/59")
    if ORIGIN is not None:
        SQL += "and origin_address='%s'" % (ORIGIN)
    SQL += "order by update_time desc"
    printlog("%s" % SQL, 2)

    printlog(SQL, 2)
    sys.stdout.flush()
    cur = conn.cursor()
    # Run query
    cur.execute(SQL)
    rows = cur.fetchall()
    nrows = len(rows)
    cur.close()
    bookings = {}

    for row in rows:
        #          2017/09/15/12/00/53
        dtime = datetime.strptime(row[0], "%Y/%m/%d/%H/%M/%S")
        #btime = str(row[0] or '')[11:16].replace("/", ":")
        btime = dtime.strftime("%Y%m%d%H%M")
        try:
            bookings[btime] += 1
        except KeyError:
            bookings[btime] = 1
        #printlog("%s = %d" % (btime, bookings[btime]),2)

    return bookings


def GraphBookings(conn, show_mins, dt1=None, dt2=None, ORIGIN=None, WIDTH=0):

    if WIDTH == 0:
        WIDTH=80

    if dt1 is not None and dt2 is not None:
        if dt2 <= dt1:
            print "Invalid time range"
            return
        bookings = InitGraphBookings(conn, dt1, dt2, ORIGIN, WIDTH)
        PrintGraph(bookings, dt1, dt2, ORIGIN, WIDTH)
        return
    elif show_mins > 0:
        dt1 = datetime.now() - timedelta(minutes=show_mins)
        dt2 = datetime.now() - timedelta(minutes=1)
    else:
        print "No date/time or period provided for booking graph"
        return

    bookings = InitGraphBookings(conn, dt1, dt2, ORIGIN, WIDTH)

    PrintGraph(bookings, dt1, dt2, ORIGIN, WIDTH)

    while True:
        try:
            # Wait for 60 seconds
            time.sleep(60)
            dt1 = datetime.now() - timedelta(minutes=show_mins)
            dt2 = datetime.now() - timedelta(minutes=1)

            SQL = "SELECT count(book_no) nbook FROM book"
            SQL += " WHERE update_time>='%s' " % dt2.strftime("%Y/%m/%d/%H/%M/00")
            SQL += " AND update_time<='%s' " % dt2.strftime("%Y/%m/%d/%H/%M/59")
            if ORIGIN is not None:
                SQL += "and origin_address='%s'" % (ORIGIN)
            printlog(SQL, 2)
            sys.stdout.flush()
            cur = conn.cursor()
            # Run query
            cur.execute(SQL)
            rows = cur.fetchall()
            nrows = len(rows)
            cur.close()

            nbook = rows[0][0]
            btime = dt2.strftime("%Y%m%d%H%M")
            bookings[btime] = nbook
            PrintGraph(bookings, dt1, dt2, ORIGIN, WIDTH)
            # Delete entry in dictionary no longer needed
            btime = dt1.strftime("%Y%m%d%H%M")
            bookings.pop(btime, None)
        except KeyboardInterrupt:
            print "\nDone"
            break
