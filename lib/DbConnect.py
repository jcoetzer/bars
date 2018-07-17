"""Connect and disconnect."""

import sys
import psycopg2
from psycopg2 import extras
from BarsLog import blogger


def OpenDb(dbname, dbuser, dbhost):
    """Open connection to database."""
    try:
        connstr = "dbname='%s' user='%s' host='%s'" \
            % (dbname, dbuser, dbhost)
        conn = psycopg2.connect(connstr)
    except:
        blogger().error("Could not connect to database: %s" % (connstr))
        sys.exit(1)
    #blogger().info("Connected to database %s" % dbname)
    return conn


def CloseDb(conn):
    """Close connection to database."""
    conn.commit()
    conn.close()
    blogger().info("Disconnected")
