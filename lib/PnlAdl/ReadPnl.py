"""
Read passenger name list.

@file ReadPnl.py
"""

from BarsLog import blogger


def ReadPnl(conn, aFlightNumber, aBoardDate):
    """
    Read PNl from database

    @param   aFlightNumber   flight number
    @param   aBoardDate      board date
    @param   inBuf           buffer
    """
    strPnlAdlMesg = ''
    iNoOfRecords = 0
    szPnlAdlMesg = ''

    blogger.info("Get PNL data for flight '%s' board '%s'"
             % (aFlightNumber, aBoardDate))
    inBuf = ''
    sqlStr = "SELECT message FROM pnl_adl_store" \
             " WHERE flight_number='%s'" \
             " AND board_date='%s'" \
             " AND pnl_adl_type = 'P'" \
             % (aFlightNumber, aBoardDate)
    blogger.debug("%s", sqlStr)
    cur = conn.cursor()
    # Fetch the input data
    cur.execute(cur)
    # TODO only the last record will be stored but there should only be one
    for row in cur:
        inBuf = str(row[0])
        blogger.info("Read %d byte" % len(inBuf))
        iNoOfRecords += 1
    blogger.info("Read %d byte" % len(inBuf))
    cur.close()
    return inBuf


def PrintPnl(pl):
    """Print PNL text."""
    pl.PnlHeader()
    pl.Show()
    pl.PnlFooter()
    print("\n")
    return 0
