# BarsLog.py

import sys

verbose = 0


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
        if lvl >= 2:
            # print("\t", end=" ")
            print "\t",
        # print("%s" % msg)
        print "%s" % msg
        sys.stdout.flush()
