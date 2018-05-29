# @file ReadRequests.py

import sys
import operator
import psycopg2  # the Informix DB module
from BarsLog import set_verbose, get_verbose, printlog


def ReadRequestsPnl(conn, book_no, Company, DeprAirport, FlightDate, PassengerName=None):

    ssrSql = \
        "SELECT DISTINCT book_requests.rqst_sequence_no seq, book_requests.indicator ind, book_requests.rqst_code rq," \
        "book_requests.action_code acc, book_requests.actn_number acn, book_requests.request_text req, book_requests.all_itenary_flag alli, " \
        "book_requests.all_passenger_flag allp" \
        " FROM book_requests, service_requests" \
        " WHERE book_requests.book_no = %d" \
        " AND book_requests.rqst_code = service_requests.rqst_code" \
        " AND service_requests.company_code = '%s'" \
        " AND book_requests.indicator = service_requests.indicator" \
        " AND service_requests.arpt_action_flag = 'Y'" \
            % (book_no, Company)
    ssrSql += \
        " UNION SELECT 0 AS rqst_sequence_no ,'F' AS indicator ,f.pnl_adl_identifier AS rqst_code, 'HK' AS action_code, '1' AS actn_number," \
        "  (trim(p.payment_form) || ' ' || abs(round(p.payment_amount, 2)*100)::integer)::varchar(60) AS request_text," \
        "  'Y' AS all_itenary_flag, 'Y' AS all_passenger_flag" \
        " FROM payments AS p" \
        " INNER JOIN FEE AS f ON f.fee_code = p.payment_form" \
        " AND p.payment_type = 'BC'" \
        " AND p.book_no = %d" \
        " AND p.document_date = '%s'" \
            % (book_no, FlightDate.strftime("%m/%d/%Y"))
    if DeprAirport is not None:
        ssrSql += \
            " AND p.document_no = '%s'" \
                % DeprAirport
    if PassengerName is not None:
        ssrSql += \
            " AND p.passenger_name = '%s'" \
                % (PassengerName)
    ssrSql += \
        " AND f.active_flag = 1" \
        " AND f.allow_segment_association = 1" \
        " AND trim(coalesce(f.pnl_adl_identifier,'')) <> ''" \
        " AND p.create_time BETWEEN f.valid_from_date_time AND coalesce(f.valid_until_date_time, current_date + interval '1' year)"
    printlog(2, ssrSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ssrSql)
    rval = ""
    n = 0
    for row in cur:
        n += 1
        print "%s %s %s %s %s %s %s %s" \
            % (row['seq'], row['ind'], row['rq'], row['acc'], row['acn'], row['req'], row['alli'], row['allp'])
    cur.close()

    return n


def ReadRequests(conn, book_no, rqst_code, delim=" ", booking_status='A'):
    d_reqs = []
    if book_no < 0:
        d_reqs.append(str("%3s%s%24s" % ("Act", delim, str("SSR code %s" % rqst_code))))
        return 0, d_reqs
    elif book_no == 0:
        d_reqs.append(str("%3s%s%24s" % ("", delim, "")))
        return 0, d_reqs
    printlog(1, "Read book requests for booking %d" % (book_no))
    ssrSql = \
        "SELECT rqst_sequence_no,rqst_code,carrier_code,action_code,actn_number,request_text," \
        " processing_flag,all_passenger_flag,all_itenary_flag " \
        " FROM book_requests WHERE book_no=%d" % book_no
    if booking_status == 'A' or booking_status == 'Y':
        ssrSql += \
            " and action_code not like 'X%'"
    elif booking_status == 'X':
        ssrSql += \
            " and action_code like 'X%'"
    else:
        pass
    ssrSql += \
        " and rqst_code='%s'" % rqst_code
    printlog(2, ssrSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ssrSql)
    rval = ""
    n = 0
    for row in cur:
        d_reqs.append(str("%2s%1s%s%24s" % (row['action_code'],row['actn_number'],delim,row['request_text'])))
        n += 1

    #printlog("%d requests" % n)
    return n, d_reqs


def ReadRequestsDaily(conn, recCount=0, start_date=None, end_date=None, dest_id=None):

    if recCount==0 and start_date is None and branch_code is None:
        print "Record count, branch code or start date must be specified"
        return
    print "SSR info"
    FiSql = \
        "SELECT"
    if recCount:
        FiSql += \
            " FIRST %d" % recCount
    FiSql += " book_no,rqst_code,action_code,actn_number,processing_flag,update_time,request_text," \
             " update_user,update_group,update_time FROM book_requests"
    FiSql += " where 1=1"
    if dest_id is not None:
        print "\tBranch code (destination ID) '%s'" % dest_id
        if '%' in dest_id or '_' in dest_id:
            FiSql += \
                " AND update_group LIKE '%s'" % dest_id
        else:
            FiSql += \
                " AND update_group='%s'" % dest_id
    if start_date is not None:
        if end_date is None:
            print "\tFor %s" % start_date.strftime("%Y-%m-%d")
            end_date = start_date
        else:
            print "\tFrom %s to %s" % (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        FiSql += \
            " AND update_time>='%s' AND update_time<='%s'" \
                % (start_date.strftime("%Y/%m/%d/00/00/00"), end_date.strftime("%Y/%m/%d/23/59/59"))

    printlog(2, FiSql)
    sys.stdout.flush()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(FiSql)
    print "%8s %5s %4s %5s %8s %20s %s" % ("Booking", "SSR", "Stat", "User", "Dest", "Update", "Text")
    for row in cur:
        print "%8d %5s %3s%1d %5s %8s %20s %s" % \
            (row['book_no'], row['rqst_code'], str(row['action_code'] or ''), int(row['actn_number'] or 0), \
            row['update_user'], row['update_group'], row['update_time'], row['request_text'])
    print


def ListRequestCodes(conn, book_no, includes='', delim=" "):
    ssrSql = \
        "SELECT distinct rqst_code " \
        "FROM book_requests WHERE book_no=%d" % book_no
    if len(includes) > 2:
        ssrSql += \
            " AND rqst_code IN (%s)" % includes
    ssrSql += \
        " AND action_code NOT LIKE 'X%'"
    printlog(2, ssrSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ssrSql)
    rval = ""
    n = 0
    for row in cur:
        if n:
            rval += delim
        rval += str("%4s" % (row['rqst_code']))
        n += 1

    printlog(1, "%d request codes" % n)
    return rval

def ReadRequestCodes(conn, book_no, delim=" "):
    d_reqs = []
    if book_no < 0:
        d_reqs.append(str("%4s%s%2s%s%-24s" % ("Code", delim, "Act", delim, "Text")))
        return 0, d_reqs
    elif book_no == 0:
        d_reqs.append(str("%4s%s%2s%s%24s" % ("", delim, "", delim, "")))
        return 0, d_reqs
    printlog(1, "Read request codes for booking %d" % (bookno), 2)
    ssrSql = \
        "SELECT rqst_sequence_no,rqst_code,carrier_code,action_code,actn_number,request_text," \
        " processing_flag,all_passenger_flag,all_itenary_flag" \
        " FROM book_requests WHERE book_no=%d" % book_no
    ssrSql += \
        " AND action_code NOT LIKE 'X%'"
    printlog(2, ssrSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ssrSql)
    rval = ""
    n = 0
    for row in cur:
        d_reqs.append(str("%4s%s%2s%d%s%-24s" \
            % (row['rqst_code'], delim, row['action_code'], int(row['actn_number']), delim, row['request_text'])))
        n += 1

    printlog(1, "%d requests" % n)
    return n, d_reqs

