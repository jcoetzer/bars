# @file BarsLog.py
"""
Implement logging stuff.
"""

import sys
import logging

verbose = 0
ilogger = None


def init_blogger(lname, verbose=0):
    """Set up logging thing."""
    global ilogger
    try:
        logging.basicConfig()
        ilogger = logging.getLogger(lname)
    except e:
        print("Logging error: %s" % str(e))
        sys.exit(1)
    if ilogger is None:
        print("Could not set up logging for %s" % lname)
        sys.exit(1)
    if verbose == 2:
        ilogger.setLevel(logging.DEBUG)
    elif verbose == 1:
        ilogger.setLevel(logging.INFO)
    else:
        pass
    # print("Start logging %s" % str(ilogger))


def blogger():
    """Get logging thing."""
    global ilogger
    return ilogger

