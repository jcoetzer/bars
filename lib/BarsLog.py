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

