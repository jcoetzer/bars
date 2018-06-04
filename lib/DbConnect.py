"""Connect and disconnect."""

import sys
import psycopg2
from BarsLog import printlog


def OpenDb(dbname, dbuser, dbhost):
    """Open connection to database."""
    try:
        connstr = "dbname='%s' user='%s' host='%s'" \
            % (dbname, dbuser, dbhost)
        conn = psycopg2.connect(connstr)
    except:
        print("Could not connect to database: %s" % (connstr))
        sys.exit(1)
    printlog(1, "Connected to database %s" % dbname)
    return conn


def CloseDb(conn):
    """Close connection to database."""
    conn.commit()
    conn.close()
    printlog(1, "Disconnected")
