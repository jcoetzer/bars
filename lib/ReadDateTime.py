# ReadDateTime.py

import sys
import time
from datetime import datetime, timedelta, date
from BarsLog import printlog


def DateRange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def ReadDateTime(arg):
    try:
        if arg is None:
            print "Empty date"
            return ''
        elif arg.lower() == 'yesterday':
            return datetime.today() - timedelta(1)
        elif arg.lower() == 'today':
            return datetime.today()
        elif arg.lower() == 'tomorrow':
            return datetime.today() + timedelta(1)
        # 20JUL
        elif len(arg) == 5:
            arg += datetime.today().strftime("%Y")
            return datetime.strptime(arg, "%d%b%Y")
        # 20JUL17
        elif len(arg) == 7:
            return datetime.strptime(arg, "%d%b%y")
        elif len(arg) == 10:
            # 07/20/2017
            if arg[2] == '/' and arg[5] == '/':
                return datetime.strptime(arg, "%m/%d/%Y")
            # 2017-07-20
            elif arg[4] == '-' and arg[7] == '-':
                return datetime.strptime(arg, "%Y-%m-%d")
            else:
                print "Invalid 10 character date '%s'" % arg
                sys.exit(1)
        elif len(arg) == 8:
            # 07/20/17
            if arg[2] == '/' and arg[5] == '/':
                return datetime.strptime(arg, "%m/%d/%y")
            elif arg[1] == '/' and arg[3] == '/':
                return datetime.strptime(arg, "%m/%d/%Y")
            # 17-07-20
            elif arg[2] == '-' and arg[5] == '-':
                return datetime.strptime(arg, "%y-%m-%d")
            else:
                print "Invalid 8 character date '%s'" % arg
                sys.exit(1)
        elif len(arg) == 9:
            if arg[2] == '/' and arg[4] == '/':
                return datetime.strptime(arg, "%m/%d/%Y")
            elif arg[1] == '/' and arg[4] == '/':
                return datetime.strptime(arg, "%m/%d/%Y")
            else:
                return datetime.strptime(arg, "%d%b%Y")
        # 20JUL17
        elif len(arg) == 7:
            return datetime.strptime(arg, "%d%b%y")
        # 2017-09-14 10:29
        elif len(arg) == 16:
            return datetime.strptime(arg, "%Y-%m-%d %H:%M")
        # 17-09-14 10:29:40
        elif len(arg) == 17:
            return datetime.strptime(arg, "%y-%m-%d %H:%M:%S")
        # 2017-09-14 10:29:40
        elif len(arg) == 19:
            return datetime.strptime(arg, "%Y-%m-%d %H:%M:%S")
        else:
            #return datetime.strptime(arg, "%Y-%m-%d")
            print "Invalid date '%s' (%d bytes)" % (arg, len(arg))
            sys.exit(1)
    except e:
        print "Could not convert datetime '%s' (%d bytes): %s" % (arg, len(arg), str(e))
        sys.exit(1)


def ReadDate(arg):
    printlog(2, "Convert date '%s'" % (str(arg)))
    try:
        if arg is None:
            print "Empty date"
            return ''
        elif arg.lower() == 'yesterday':
            return datetime.today() - timedelta(1)
        elif arg.lower() == 'today':
            return datetime.today()
        elif arg.lower() == 'tomorrow':
            return datetime.today() + timedelta(1)
        # 20JUL
        elif len(arg) == 5:
            arg += datetime.today().strftime("%Y")
            return datetime.strptime(arg, "%d%b%Y")
        # 20JUL17
        elif len(arg) == 7:
            return datetime.strptime(arg, "%d%b%y").date()
        elif len(arg) == 8:
            # 07/20/17
            if arg[2] == '/' and arg[5] == '/':
                return datetime.strptime(arg, "%m/%d/%y").date()
            elif arg[1] == '/' and arg[3] == '/':
                return datetime.strptime(arg, "%m/%d/%Y").date()
            # 17-07-20
            elif arg[2] == '-' and arg[5] == '-':
                return datetime.strptime(arg, "%y-%m-%d").date()
            else:
                print "Invalid 8 character date '%s'" % arg
                sys.exit(1)
        elif len(arg) == 9:
            if arg[2] == '/' and arg[4] == '/':
                return datetime.strptime(arg, "%m/%d/%Y").date()
            elif arg[1] == '/' and arg[4] == '/':
                return datetime.strptime(arg, "%m/%d/%Y").date()
            else:
                return datetime.strptime(arg, "%d%b%Y").date()
        elif len(arg) == 10:
            # 07/20/2017
            if arg[2] == '/' and arg[5] == '/':
                return datetime.strptime(arg, "%m/%d/%Y").date()
            # 2017-07-20
            elif arg[4] == '-' and arg[7] == '-':
                return datetime.strptime(arg, "%Y-%m-%d").date()
            else:
                print "Invalid 10 character date '%s'" % arg
                sys.exit(1)
        # 2017-09-14 10:29
        elif len(arg) == 16:
            return datetime.strptime(arg, "%Y-%m-%d %H:%M").date()
        # 17-09-14 10:29:40
        elif len(arg) == 17:
            return datetime.strptime(arg, "%y-%m-%d %H:%M:%S").date()
        # 2017-09-14 10:29:40
        elif len(arg) == 19:
            return datetime.strptime(arg, "%Y-%m-%d %H:%M:%S").date()
        else:
            #return datetime.strptime(arg, "%Y-%m-%d")
            print "Invalid date '%s' (%d bytes)" % (arg, len(arg))
            sys.exit(1)
    except:
        print "Could not convert date '%s' (%d bytes)" % (arg, len(arg))
        sys.exit(1)


def ReadTime(arg):
    try:
        atime = None
        printlog(2, "Convert time '%s'" % (str(arg)))

        if type(arg) is str:
            atime = arg[0:5]
        else:
            atime = "%02d:%02d" % (int(arg/100), int(arg%100))
        printlog(2, "Time is %s" % atime)
        return time.strptime(atime, "%H:%M")
    except:
        print "Could not convert time %s (%s)" % (arg, atime)
        sys.exit(1)

