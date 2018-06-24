"""
Read passenger name list.

@file ReadPnl.py
"""

from BarsLog import printlog


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

    printlog(1, "Get PNL data for flight '%s' board '%s'"
             % (aFlightNumber, aBoardDate))
    inBuf = ''
    sqlStr = "SELECT message FROM pnl_adl_store" \
             " WHERE flight_number='%s'" \
             " AND board_date='%s'" \
             " AND pnl_adl_type = 'P'" \
             % (aFlightNumber, aBoardDate)
    printlog(2, "%s", sqlStr)
    cur = conn.cursor()
    # Fetch the input data
    cur.execute(cur)
    # TODO only the last record will be stored but there should only be one
    for row in cur:
        inBuf = str(row[0])
        printlog(1, "Read %d byte" % len(inBuf))
        iNoOfRecords += 1
    printlog(1, "Read %d byte" % len(inBuf))
    cur.close()
    return inBuf


def PrintPnl(pl):
    """Print PNL text."""
    pl.PnlHeader()
    pl.Show()
    pl.PnlFooter()
    print("\n")
    return 0
