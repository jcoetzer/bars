"""Connect and disconnect."""

import sys
import logging
import psycopg2
from psycopg2 import extras


logger = logging.getLogger("web2py.app.bars")


def OpenDb(dbname, dbuser, dbhost):
    """Open connection to database."""
    try:
        connstr = "dbname='%s' user='%s' host='%s'" \
            % (dbname, dbuser, dbhost)
        conn = psycopg2.connect(connstr)
    except:
        logger.error("Could not connect to database: %s" % (connstr))
        sys.exit(1)
    #logger.info("Connected to database %s" % dbname)
    return conn


def CloseDb(conn):
    """Close connection to database."""
    conn.commit()
    conn.close()
    logger.info("Disconnected")
