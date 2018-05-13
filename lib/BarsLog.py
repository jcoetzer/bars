# BarsLog.py

import sys
import time
from datetime import datetime, timedelta, date

verbose = 0


def set_verbose(lvl):

    global verbose

    verbose = lvl


def get_verbose():

    global verbose

    return verbose


def printlog(lvl, msg):

    global verbose

    if verbose >= lvl:
        if lvl >= 2: print "\t",
        print "%s" % msg
        sys.stdout.flush()


