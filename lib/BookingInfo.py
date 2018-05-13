# @file BookingInfo.py
"""
Data for bookings.

Various inserts.
"""

# import psycopg2

import string
from BarsLog import printlog

digs = string.ascii_uppercase + string.digits
digs20 = 'BCDFGHJKLMNPQRSTVWXYZ'


def int2base(x, base, adigs=digs):
    """
    Convert number to arbitrary base.

    Return string.

    """
    if x < 0:
        sign = -1
    elif x == 0:
        return adigs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(adigs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


def int2base20(x):
    """Convert integer to base 20 number."""
    return int2base(x, 20, digs20)


def AddBook(conn, aSeatQuantity, aOriginBranchCode, aAgencyCode, aFlightDate,
            aUser, aGroup):
    """
    Add entry to book table.

    Return booking number.
    """
    abSql = \
        "INSERT INTO book(pnr_book_numb, book_type, group_name, no_of_seats," \
        "book_category, grup_wait_seats, grup_rqst_seats, grup_realtn_pcnt, origin_branch_code," \
        "book_agency_code, received_from, tour_code, amount_paid, booking_status, scrutiny_flg," \
        "first_segm_date, last_segm_date, reaccom_prty, dvd_process_flg, rdu_process_flg," \
        "grp_process_flg, nrl_process_flg, crea_user_code, crea_dest_id, create_time," \
        "user_name, user_group, update_time) VALUES (NULL, 'R', 'NTBA/A', '%s', 'G', 0, 0, 0, '%s'  ," \
        "'%s', '%s', 'ALLOTMENT', 0, 'Y', 'N', '%s', '%s', 0, 'Y', 'Y', 'Y', 'Y', '%s', '%s', NOW(), '%s', '%s', NOW())" \
        " RETURNING book_no" \
        % (aSeatQuantity, aOriginBranchCode, aAgencyCode, aUser, aFlightDate,
           aFlightDate, aUser, aGroup, aUser, aGroup)
    printlog(2, "%s" % abSql)
    cur = conn.cursor()
    cur.execute(abSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)

    rv = 0
    for row in cur:
        rv = int(row[0])

    printlog(1, "New booking number %d" % rv)
    vPnr = int2base20(rv)
    abSql = \
        "UPDATE book SET pnr_book_numb='%s' WHERE book_no=%d" % (vPnr, rv)
    printlog(2, "%s" % abSql)
    cur.execute(abSql)
    printlog(2, "Updated %d row(s)" % cur.rowcount)
    return rv


def AddItenary(conn, aBookNo,
               aFlightNumber, aFlightDate,
               aDepart, aArrive,
               aDepartTime, aArriveTime,
               aDepartTerm, aArriveTerm,
               aCityPair, aSellClass, aUser, aGroup):
    """Add entry for itenary."""
    dateChangeInd = 0
    flightPathCode = aDepart[0]
    physicalClass = 'Y'
    # itenaryStatus = 'A'
    # itenaryType = 'I'
    # reserveStatus = 'HK'
    # fareNumber = 1
    actionToCompany = aFlightNumber[0:2]
    aiSql = "INSERT INTO itenary(book_no," \
            "route_no,alt_itenary_no,itenary_no," \
            "flight_number,flight_date," \
            "departure_city,arrival_city,depr_airport,arrv_airport," \
            "departure_time,arrival_time,date_change_ind,flight_path_code," \
            "depr_terminal_no,arrv_terminal_no,city_pair_no," \
            "physical_cls_code,selling_cls_code," \
            "itenary_stat_flag,itenary_type,reserve_status," \
            "fare_nos,processing_flg,rlr_rqr_count," \
            "action_to_company,updt_user_code,updt_dest_id,updt_date_time)" \
            " VALUES (" \
            "%d, 1, 1, 0," \
            " '%s', '%s', '%s', '%s', '%s', '%s', " \
            " '%s', '%s', '%s', '%s'," \
            " '%s', '%s', %s," \
            " '%s', '%s'," \
            " 'A', 'R', 'GK#GR', 0, 'N', 0," \
            " '%s', '%s', '%s', NOW())" \
            % (aBookNo,
               aFlightNumber, aFlightDate, aDepart, aArrive, aDepart, aArrive,
               aDepartTime, aArriveTime, dateChangeInd, flightPathCode,
               aDepartTerm, aArriveTerm, aCityPair,
               physicalClass, aSellClass,
               actionToCompany, aUser, aGroup)
    printlog(2, "%s" % aiSql)
    cur = conn.cursor()
    cur.execute(aiSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def GetPreBookingInfo(conn, book_no, ):
    """Query to run sometimes."""
    preBookingInfoSql = """
        select bo.book_no,bo.pnr_book_numb,
            case when (bo.group_name is null or bo.group_name='') then (select pax.passenger_name from passenger as pax where pax.book_no=bo.book_no and pax.passenger_no=0) else bo.group_name end as group_name
            bo.book_agency_code,
            bo.crea_date_time,
            bo.booking_status,
            bo.no_of_seats,
            bo.book_category,
            ta.trade_name as agency_trade_name,
            bci.ext_book_numb as external_book_number,
            bo.origin_address as origin_address,
            select count(*) from queues as qu where qu.queue_code='TTREJ' and qu.book_no=bo.book_no and qu.processing_flg<>'Y')
                as tty_reject_indicator,
            select count(*) from end_transaction as et where et.key_no=bo.book_no and et.processing_flg='R')
                as et_reject_indicator,
            bo.scrutiny_flg as scrutiny_flag,
            select count(*) from end_transaction as et where et.key_no=bo.book_no and et.processing_flg='N')
                as et_queue_count,
            select count(*) from tty_in_mesgs as tim where tim.book_no=bo.book_no and tim.processing_flg in ('N','U'))
                as tty_in_queue_count,
            select min(btl.limit_date::datetime year to minute + btl.limit_time_mns units minute) as last_payment_date_time
                        from book_time_limits as btl
                        where btl.book_no = bo.book_no
                        and btl.timelmt_type = 'T'
                        and btl.cancel_flg = 'C'
                        and not exists (select * from payments as pay where pay.book_no = bo.book_no and pay.paid_flg = 'Y' and pay.payment_amount > 0)
            as last_payment_date_time,
            select min(bav.field_value_string) as fare_designator
                    from book_additional_data_field_value as bav
                    inner join book_additional_data_field as baf on baf.book_additional_data_field_id = bav.book_additional_data_field_id
                    where bav.book_no = bo.book_no
                    and (baf.application_field_code='FareDesignator' or baf.field_name='FareDesignator')
            as fare_designator
        from book as bo
        left join travel_agency  as ta  on ta.agency_code = bo.book_agency_code
        left join book_crs_index as bci on bci.book_no = bo.book_no
        where bo.book_no = %d """ \
        % (book_no)
    printlog(2, "%s" % preBookingInfoSql)
    cur = conn.cursor()
    cur.execute(preBookingInfoSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    for row in cur:
        book_no = row[0]
        pnr_book_numb = row[1]
        group_name = row[2]
        book_agency_code = row[3]
        crea_date_time = row[4]
        booking_status = row[5]
        print("Book %d PNR %s agency %s time %s status %s" % (book_no, pnr_book_numb, group_name,
                                                              book_agency_code, crea_date_time, booking_status))


def AddBookFares(conn, aBookNo, aFareNo, aPaxCode, aDepart, aArrive, aCurrency, aAmount, aUser, aGroup):
    """Add entry for book fare."""
    abfSql = """
        INSERT INTO book_fares( book_no, fare_no, pass_code,
                                start_city, end_city, total_amount_curr, total_amount,
                                fare_construction, endrsmnt_rstrctns, fare_stat_flg,
                                updt_user_code, updt_dest_id, updt_date_time )
        VALUES(%d, %d, '%s',
               '%s', '%s', '%s', '%f',
               '-', '-', 'S',
               '%s', '%s', NOW() )""" \
             % (aBookNo, aFareNo, aPaxCode,
                aDepart, aArrive, aCurrency, aAmount,
                aUser, aGroup)
    printlog(2, "%s" % abfSql)
    cur = conn.cursor()
    cur.execute(abfSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def AddBookFareSegments(conn, aBookNo, aFareNo, aPaxCode, aFlight, aDate,
                        aDepart, aArrive, aCurrency, aAmount, aUser, aGroup):
    """Add entry for book fare segment."""
    abfSql = """
        INSERT INTO book_fares_segm(book_no, fare_no, pass_code,
                                    flight_number, board_date,
                                    depr_airport, arrv_airport,
                                    selling_cls_code, fare_basis,
                                    valid_from_date, valid_to_date,
                                    updt_user_code, updt_dest_id,
                                    updt_date_time)
        VALUES(%d, %d, '%s',
               '%s', '%s',
               '%s', '%s',
               '%s', '%s',
               '%s', '%s',
               '%s', '%s',
               NOW())""" \
            % (aBookNo, aFareNo, aPaxCode,
               aFlight, aDate,
               aDepart, aArrive,
               aCurrency, aAmount,
               aDate, aDate,
               aUser, aGroup)
    printlog(2, "%s" % abfSql)
    cur = conn.cursor()
    cur.execute(abfSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def AddBookFarePassengers(conn, aBookNo, aPaxCode, aCurrency, aAmount,
                          aUser, aGroup):
    """Add entry for book fare passenger."""
    vFare = ' '
    vRestrict = ' '
    abfSql = """
        INSERT INTO book_fares_pass(book_no, pass_code,
                                    total_amount_curr, total_amount,
                                    fare_construction, endrsmnt_rstrctns,
                                    updt_user_code, updt_dest_id,
                                    updt_date_time)
        VALUES ( %d, '%s',
                 '%s', %f,
                 '%s', '%s',
                 '%s', '%s',
                 NOW() ) """ \
        % (aBookNo, aPaxCode, aCurrency, aAmount, vFare, vRestrict,
           aUser, aGroup)
    printlog(2, "%s" % abfSql)
    cur = conn.cursor()
    cur.execute(abfSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def AddBookFaresPayments(conn, aBookNo, aFareNo, aPaxCode, aFareCode,
                         aCurrency, aAmount, aUser, aGroup, aSource):
    """Add entry for book fare payment."""
    abfSql = """
        INSERT INTO book_fares_paym( book_no, fare_no, pass_code,
                                     payment_code, fare_calc_code,
                                     paid_curr_code, fare_paymt_amt,
                                     tax_code, nation_code,
                                     refund_stat_flag, exempt_stat_flag,
                                     net_fare_flag, private_fare_flag,
                                     refundable_flag,
                                     updt_user_code, updt_dest_id, updt_date_time, source_ref_id )
        VALUES ( '%s', '%s', '%s',
                 'FEE', '%s',
                 '%s', %f,
                 '', '',
                 'N', 'N',
                 'N', 'N',
                 'N',
                 '%s', '%s', NOW(), '%s' ) """ \
        % (aBookNo, aFareNo, aPaxCode, aFareCode, aCurrency, aAmount, aUser, aGroup, aSource)
    printlog(2, "%s" % abfSql)
    cur = conn.cursor()
    cur.execute(abfSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def AddBookRequest(conn, aBookNo, aCompany, aReqCode, aReqText, aUser, aGroup):
    """Add book request."""
    # TODO value for rqst_seqn_no is dodgy
    # (select nvl(max(rqst_seqn_no),0)+1 from book_requests where book_no = %d)
    vRequestSeq = 1
    abrSql = \
        """
        INSERT INTO book_requests ( book_no,
                                    rqst_seqn_no,
                                    item_no, indicator, rqst_code,
                                    carrier_code,
                                    action_code, actn_number,
                                    processing_flg, rqr_count,
                                    request_text,
                                    all_passenger_flg, all_itenary_flg,
                                    updt_user_code, updt_dest_id,
                                    updt_date_time )
        VALUES ( %d,
                 %d,
                 1, 'S', '%s',
                 '%s',
                 'HK', '1', 'Y', 1,
                 '%s',
                 'N', 'Y',
                 '%s', '%s', NOW() )""" \
        % (aBookNo, vRequestSeq, aReqCode, aCompany, aReqText, aUser, aGroup)
    printlog(2, "%s" % abrSql)
    cur = conn.cursor()
    cur.execute(abrSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def AddPassenger(conn, aBookNo, aPaxNo,
                 aPaxName,
                 aPaxCode, aProcFlag,
                 aUser, aGroup):
    """Add passenger record."""
    vClientProfileNo = ' '
    vFareNo = ' '
    vTimeLimitNo = ' '
    vTtyLineNo = 0
    vTtyGrpNo = 0
    vTtyGrpSeq = 0
    apSql = """
        INSERT INTO passenger( book_no,passenger_no,passenger_name,
            client_prfl_no, request_nos,remark_nos, fare_nos,
            contact_nos,timelmt_nos,ticket_nos,name_incl_type,pass_code,processing_flg,
            updt_user_code, updt_dest_id, updt_date_time,
            tty_pax_line_no, tty_pax_grp_no, tty_pax_grp_seq )
        VALUES (%d, %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', NOW(), %d, %d, %d)""" \
        % (aBookNo, aPaxNo,
           aPaxName,
           vClientProfileNo,
           " ", " ", vFareNo, " ",
           vTimeLimitNo, " ", " ",
           aPaxCode, aProcFlag,
           aUser, aGroup,
           vTtyLineNo, vTtyGrpNo, vTtyGrpSeq)
    printlog(2, "%s" % apSql)
    cur = conn.cursor()
    cur.execute(apSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


def AddPayment(conn, aPaymentForm, aPaymentType, aCurrency, aAmount,
               aDocNum, aPaymentMode,
               aBookNo, aPaxName, aPaxCode,
               aBranchCode, aRemark,
               aUser, aGroup):
    """Add payment entry."""
    apSql = """
        INSERT INTO payments(
                payment_form, payment_type,
                paid_curr_code, payment_amount,
                payment_date, document_no, payment_mode,
                book_no, passenger_name, pass_code,
                origin_branch_code, remarks_text, received_from,
                paid_flg, pay_stat_flg, recpt_stat_flg, invc_stat_flg, payment_ind,
                create_user, create_group, create_time,
                update_user, update_group, update_time)
        VALUES ('%s', '%s',
                '%s', %s,
                CURRENT_DATE, '%s', '%s',
                %d, '%s', '%s',
                '%s', '%s', ' ',
                'Y', 'A', 'A', 'A', 'Y',
                '%s', '%s', NOW(),
                '%s', '%s', NOW()
                )""" \
        % (aPaymentForm, aPaymentType,
           aCurrency, aAmount,
           aDocNum, aPaymentMode,
           aBookNo, aPaxName, aPaxCode,
           aBranchCode, aRemark,
           aUser, aGroup,
           aUser, aGroup)
    printlog(2, "%s" % apSql)
    cur = conn.cursor()
    cur.execute(apSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
