# @file BarsLog.py
"""
Implement logging stuff.
"""

import sys
import logging

verbose = 0
blogger = None

def init_blogger(lname):
    """Set up logging thing."""
    global blogger
    blogger = logging.getLogger(lname)
    blogger.setLevel(logging.DEBUG)


def set_verbose(lvl):
    """Set logging level."""
    global verbose

    verbose = lvl


def get_verbose():
    """Get logging level."""
    global verbose

    return verbose


def printlog(lvl, msg):
    """Log message."""
    global verbose

    if verbose >= lvl:
        #if lvl >= 2:
            #print("\t", end=" ")
        print("%s" % msg)
        sys.stdout.flush()
