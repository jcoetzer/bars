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


def AddBookCrossIndex(conn, aBookCategory, aOriginAddress, aUser, aGroup):
    """Add booking cross reference."""
    abSql = """
        INSERT INTO book_cross_index (
            pnr_book_numb, origin_address, book_category,
            processing_flg, update_user, update_group, update_time)
        VALUES (
            '------', '%s', '%s', 'A', '%s', '%s', NOW() )
        RETURNING book_no""" \
        % (aOriginAddress, aBookCategory, aUser, aGroup)
    printlog(2, "%s" % abSql)
    cur = conn.cursor()
    cur.execute(abSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)

    vBookNo = 0
    for row in cur:
        vBookNo = int(row[0])

    printlog(1, "New booking number %d" % vBookNo)
    vPnr = int2base20(vBookNo)
    abSql = \
        "UPDATE book_cross_index SET pnr_book_numb='%s' WHERE book_no=%d" \
        % (vPnr, vBookNo)
    printlog(2, "%s" % abSql)
    cur.execute(abSql)
    printlog(2, "Updated %d row(s)" % cur.rowcount)
    cur.close()
    return vBookNo, vPnr


def AddBook(conn, aBookNo, aPnr, aSeatQuantity, aOriginAddress,
            aBookCategory,
            aOriginBranchCode, aAgencyCode,
            aFlightDate,
            aUser, aGroup):
    """
    Add entry to book table.

    Return booking number.
    """
    abSql = """
        INSERT INTO book(
            book_no, pnr_book_numb, book_type, group_name,
            no_of_seats,
            book_category, grup_wait_seats, grup_rqst_seats, grup_realtn_pcnt,
            origin_address, origin_branch_code,
            agency_code, received_from, tour_code, amount_paid,
            booking_status, scrutiny_flg,
            first_segm_date, last_segm_date, reaccom_prty, dvd_process_flg,
            rdu_process_flg, grp_process_flg, nrl_process_flg,
            create_user, create_group, create_time,
            update_user, update_group, update_time )
        VALUES (
            %d, '%s', 'R', 'NTBA/A',
            %d,
            '%s', 0, 0, 0,
            '%s', '%s',
            '%s', '%s', 'ALLOTMENT', %.2f,
            'Y', 'N',
            '%s', '%s', 0, 'Y',
            'Y', 'Y', 'Y',
            '%s', '%s', NOW(),
            '%s', '%s', NOW() )""" \
        % (aBookNo, aPnr, aSeatQuantity,
           aBookCategory,
           aOriginAddress, aOriginBranchCode,
           aAgencyCode, aUser, 0.0,
           aFlightDate, aFlightDate,
           aUser, aGroup,
           aUser, aGroup)
    printlog(2, "%s" % abSql)
    cur = conn.cursor()
    cur.execute(abSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)


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
    aiSql = """
        INSERT INTO itenary(
            book_no,
            route_no,alt_itenary_no,itenary_no,
            flight_number,flight_date,
            departure_city,arrival_city,depr_airport,arrv_airport,
            departure_time,arrival_time,date_change_ind,flight_path_code,
            depr_terminal_no,arrv_terminal_no,city_pair_no,
            physical_cls_code,selling_cls_code,
            itenary_stat_flag,itenary_type,reserve_status,
            fare_nos,processing_flg,rlr_rqr_count,
            action_to_company,update_user,update_group,update_time )
         VALUES (
            %d,
            1, 1, 0,
            '%s', '%s', '%s', '%s', '%s', '%s',
            '%s', '%s', '%s', '%s',
            '%s', '%s', %s,
            '%s', '%s',
            'A', 'R', 'GK#GR', 0, 'N', 0,
            '%s', '%s', '%s', NOW() )""" \
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
    cur.close()


def AddBookTimeLimit(conn, aBookNo, aDestBranch, aUser, aGroup):
    """Add entry for booking time limit."""
    btlSql = """
        INSERT INTO book_time_limits(
            book_no, timelmt_seqn_no, timelmt_type,
            cancel_flg, dest_branch, all_passenger_flg, processing_flg,
            update_user, update_group, update_time )
        VALUES (
            %d, 1, 'T',
            'C', '%s', 'Y', 'A',
            '%s', '%s', NOW())""" \
        % (aBookNo,
           aDestBranch,
           aUser, aGroup)
    printlog(2, "%s" % btlSql)
    cur = conn.cursor()
    cur.execute(btlSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddBookFares(conn, aBookNo, aFareNo, aPaxCode, aDepart, aArrive,
                 aCurrency, aAmount, aUser, aGroup):
    """Add entry for book fare."""
    abfSql = """
        INSERT INTO book_fares(
            book_no, fare_no, pass_code,
            start_city, end_city, total_amount_curr, total_amount,
            fare_construction, endrsmnt_rstrctns, fare_stat_flg,
            update_user, update_group, update_time )
        VALUES (
            %d, %d, '%s',
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
    cur.close()


def AddBookFareSegments(conn, aBookNo, aFareNo, aPaxCode, aFlight, aDate,
                        aDepart, aArrive, aCurrency, aAmount, aUser, aGroup):
    """Add entry for book fare segment."""
    abfSql = """
        INSERT INTO book_fares_segm(
            book_no, fare_no, pass_code,
            flight_number, board_date,
            depr_airport, arrv_airport,
            selling_cls_code, fare_basis,
            valid_from_date, valid_to_date,
            update_user, update_group,
            update_time )
        VALUES (
            %d, %d, '%s',
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
    cur.close()


def AddBookFarePassengers(conn, aBookNo, aPaxCode, aCurrency, aAmount,
                          aUser, aGroup):
    """Add entry for book fare passenger."""
    vFare = ' '
    vRestrict = ' '
    abfSql = """
        INSERT INTO book_fares_pass(
            book_no, pass_code,
            total_amount_curr, total_amount,
            fare_construction, endrsmnt_rstrctns,
            update_user, update_group,
            update_time )
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
    cur.close()


def AddBookFaresPayments(conn, aBookNo, aFareNo, aPaxCode, aFareCode,
                         aCurrency, aAmount, aUser, aGroup, aSource):
    """Add entry for book fare payment."""
    abfSql = """
        INSERT INTO book_fares_paym(
            book_no, fare_no, pass_code,
            payment_code, fare_calc_code,
            paid_curr_code, fare_paymt_amt,
            tax_code, nation_code,
            refund_stat_flag, exempt_stat_flag,
            net_fare_flag, private_fare_flag,
            refundable_flag,
            update_user, update_group, update_time,
            source_ref_id )
        VALUES ( '%s', '%s', '%s',
                 'FEE', '%s',
                 '%s', %f,
                 '', '',
                 'N', 'N',
                 'N', 'N',
                 'N',
                 '%s', '%s', NOW(), '%s' ) """ \
        % (aBookNo, aFareNo, aPaxCode,
           aFareCode,
           aCurrency, aAmount,
           aUser, aGroup, aSource)
    printlog(2, "%s" % abfSql)
    cur = conn.cursor()
    cur.execute(abfSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddBookRequest(conn, aBookNo, aCompany, aReqCode, aReqTexts, aUser, aGroup):
    """Add book request."""
    # Value for request sequence number
    cur = conn.cursor()
    abrSql = "SELECT MAX(rqst_seqn_no) FROM book_requests WHERE book_no = %d" \
             % aBookNo
    printlog(2, "%s" % abrSql)
    cur.execute(abrSql)
    vRequestSeq = 0
    for row in cur:
        vRequestSeq = row[0]
    if vRequestSeq is None:
        vRequestSeq = 0
    for aReqText in aReqTexts:
        vRequestSeq += 1
        abrSql = """
            INSERT INTO book_requests (
                book_no, rqst_seqn_no,
                item_no, indicator, rqst_code,
                carrier_code,
                action_code, actn_number,
                processing_flg, rqr_count,
                request_text,
                all_passenger_flg, all_itenary_flg,
                update_user, update_group,
                update_time )
            VALUES ( %d, %d,
                     1, 'S', '%s',
                     '%s',
                     'HK', '1', 'Y', 1,
                     '%s',
                     'N', 'Y',
                     '%s', '%s', NOW() )""" \
            % (aBookNo, vRequestSeq, aReqCode, aCompany, aReqText,
               aUser, aGroup)
        printlog(2, "%s" % abrSql)
        cur.execute(abrSql)
        printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddPassenger(conn, aBookNo,
                 aPaxNames,
                 aPaxCode, aProcFlag,
                 aUser, aGroup):
    """Add passenger record."""
    vClientProfileNo = ' '
    vFareNo = ' '
    vTimeLimitNo = ' '
    vTtyLineNo = 0
    vTtyGrpNo = 0
    vTtyGrpSeq = 0
    cur = conn.cursor()
    vPaxNo = 0
    for aPaxName in aPaxNames:
        vPaxNo += 1
        apSql = """
            INSERT INTO passenger(
                book_no, passenger_no, passenger_name,
                client_prfl_no, request_nos, remark_nos, fare_nos,
                contact_nos, timelmt_nos, ticket_nos, name_incl_type, pass_code, processing_flg,
                update_user, update_group, update_time,
                tty_pax_line_no, tty_pax_grp_no, tty_pax_grp_seq )
            VALUES (%d, %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', NOW(), %d, %d, %d)""" \
            % (aBookNo, vPaxNo,
               aPaxName,
               vClientProfileNo,
               " ", " ", vFareNo, " ",
               vTimeLimitNo, " ", " ",
               aPaxCode, aProcFlag,
               aUser, aGroup,
               vTtyLineNo, vTtyGrpNo, vTtyGrpSeq)
        printlog(2, "%s" % apSql)
        cur.execute(apSql)
        printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


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
    cur.close()


def GetPreBookingInfo(conn, book_no):
    """Query to run sometimes."""
    printlog(2, "Pre booking info %d" % book_no)
    preBookingInfoSql = """
        SELECT bo.book_no,
            bo.pnr_book_numb,
            bo.group_name,
            ( SELECT pax.passenger_name
              FROM passenger AS pax
              WHERE pax.book_no=bo.book_no AND pax.passenger_no=1),
            bo.agency_code,
            bo.create_time,
            bo.booking_status,
            bo.no_of_seats,
            bo.book_category,
            ta.trade_name,
            bci.ext_book_numb,
            bo.origin_address,
            bo.scrutiny_flg,
            ( SELECT min(btl.limit_time)
              FROM book_time_limits AS btl
              WHERE btl.book_no = bo.book_no
              AND btl.timelmt_type = 'T'
              AND btl.cancel_flg = 'C'
              AND NOT EXISTS (
                    SELECT pay.book_no FROM payments AS pay
                    WHERE pay.book_no = bo.book_no
                    AND pay.paid_flg = 'Y'
                    AND pay.payment_amount > 0 ) )
        FROM book AS bo
        LEFT JOIN travel_agency AS ta ON ta.agency_code = bo.agency_code
        LEFT JOIN book_cross_index AS bci ON bci.book_no = bo.book_no
        WHERE bo.book_no = %d """ \
        % (book_no)
    printlog(2, "%s" % preBookingInfoSql)
    cur = conn.cursor()
    cur.execute(preBookingInfoSql)

    printlog(2, "Selected %d row(s)" % cur.rowcount)
    for row in cur:
        # for val in row:
            # print("%s" % str(val), end=' ')
        book_no = row[0]
        pnr_book_numb = row[1]
        group_name = row[2]
        agency_code = row[4]
        crea_date_time = row[5]
        booking_status = row[6]
        print("Book %d PNR %s group %s agency %s time %s status %s"
              % (book_no, pnr_book_numb, group_name.strip(), agency_code,
                 crea_date_time, booking_status))
    cur.close()
