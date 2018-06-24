# @file BookingInfo.py
"""
Data for bookings.

Various inserts.
"""

import psycopg2
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
            pax_name_rec, origin_address, book_category,
            processing_flag, update_user, update_group, update_time)
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
        "UPDATE book_cross_index SET pax_name_rec='%s' WHERE book_no=%d" \
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
    Add entry to bookings table.

    Return booking number.
    """
    abSql = """
        INSERT INTO bookings(
            book_no, pax_name_rec, book_type, group_name,
            no_of_seats,
            book_category, group_wait_seats, group_request_seats,
            group_realtn_pcnt,
            origin_address, origin_branch_code,
            agency_code, received_from, tour_code, payment_amount,
            status_flag, scrutiny_flag,
            first_segm_date, last_segm_date, reaccom_party, dvd_process_flag,
            rdu_process_flag, grp_process_flag, nrl_process_flag,
            create_user, create_group, create_time,
            update_user, update_group, update_time )
        VALUES (
            %d, '%s', 'R', '',
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


def AddItinerary(conn, aBookNo,
               aFlightNumber, aFlightDate,
               aDepart, aArrive,
               aDepartTime, aArriveTime,
               aDepartTerm, aArriveTerm,
               aCityPair, aSellClass, aUser, aGroup):
    """Add entry for itinerary."""
    printlog(2, "Itinerary for booking %d: flight %s date %s depart %s %s (%s) arrive %s %s (%s)"
             % (aBookNo, aFlightNumber, aFlightDate,
                aDepart, aDepartTime, aDepartTerm,
                aArrive, aArriveTime, aArriveTerm))
    dateChangeInd = 0
    flightPathCode = aDepart[0]
    physicalClass = 'Y'
    # itineraryStatus = 'A'
    # itineraryType = 'I'
    # reserveStatus = 'HK'
    # fareNumber = 1
    actionToCompany = aFlightNumber[0:2]
    aiSql = """
        INSERT INTO itineraries(
            book_no,
            route_no,alt_itinerary_no,itinerary_no,
            flight_number,flight_date,
            departure_city,arrival_city,departure_airport,arrival_airport,
            departure_time,arrival_time,date_change_ind,flight_path_code,
            departure_terminal,arrival_terminal,city_pair,
            physical_class,selling_class,
            status_flag,itinerary_type,reserve_status,
            fare_nos,processing_flag,rlr_rqr_count,
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
            book_no, timelmt_sequence_no, timelmt_type,
            cancel_flag, dest_branch, all_pax_flag, processing_flag,
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
    """Add entry for booking fare."""
    cur = conn.cursor()
    printlog(1, "Add booking %d fare %d code %s depart %s arrive %s amount %s%d"
             % (aBookNo, aFareNo, aPaxCode, aDepart, aArrive,
                aCurrency, aAmount))
    abfSql = """UPDATE book_fares SET (
            departure_airport, arrival_airport, total_amount_curr, total_amount,
            fare_construction, endrsmnt_rstrctns, status_flag,
            update_user, update_group, update_time )
        = ('%s', '%s', '%s', '%f',
           '-', '-', 'A',
           '%s', '%s', NOW() )
        WHERE book_no = %d
        AND fare_no = %d
        AND pax_code = '%s'
        """ \
        % (aDepart, aArrive, aCurrency, aAmount,
           aUser, aGroup, aBookNo, aFareNo, aPaxCode)
    cur.execute(abfSql)
    if cur.rowcount > 0:
        printlog(0, "Payment for booking %d fare %d code %s has been processed"
                 % (aBookNo, aFareNo, aPaxCode))
        cur.close()
        return

    abfSql = """
        INSERT INTO book_fares(
            book_no, fare_no, pax_code,
            departure_airport, arrival_airport, total_amount_curr, total_amount,
            fare_construction, endrsmnt_rstrctns, status_flag,
            update_user, update_group, update_time )
        VALUES (
            %d, %d, '%s',
           '%s', '%s', '%s', '%f',
           '-', '-', 'A',
           '%s', '%s', NOW() )""" \
         % (aBookNo, aFareNo, aPaxCode,
            aDepart, aArrive, aCurrency, aAmount,
            aUser, aGroup)
    printlog(2, "%s" % abfSql)
    try:
        cur.execute(abfSql)
        printlog(2, "Inserted %d row(s)" % cur.rowcount)
    except psycopg2.IntegrityError:
        printlog(0, "Payment for booking %d fare %d code %s has been processed before"
                 % (aBookNo, aFareNo, aPaxCode))
    cur.close()


def AddBookingFareSegments(conn, aBookNo, aFareNo, aPaxCode,
                           aDepart, aArrive,
                           aFlight, aFlightDate,
                           aStartDate, aEndDate,
                           aSellClass, aFareBasis,
                           aCurrency, aAmount,
                           aUser, aGroup):
    """
    Add entry for booking fare segment.

    A fare basis code is an alphabetic or alpha-numeric code used by airlines
    to identify a fare type and allow airline staff and travel agents to find
    the rules applicable to that fare. There are some patterns that have
    evolved over the years and may still be in use.

    Fare codes start with a letter called a booking class (indicating travel
    class among other things) which matches the letter code that the
    reservation is booked in. Other letters or numbers follow. Typically a fare
    basis will be 3 to 7 characters long, but can be up to 8.

    Booking code    Meaning
    F               full-fare First class
    J               full-fare Business class
    W               full-fare Premium Economy class
    Y               full-fare Economy class

    E               Second letter
        Excursion Fare: has a minimum and maximum stay requirement to encourage
        use by the holiday market and not business travellers.
    NUMERALS          Latter parts of the fare basis
        Numerals indicate the maximum stay the fare rules will allow at a
        destination. Thus a YE45 is an economy excursion fare with a maximum
        stay of 45 days. Similar patterns could be YE3M indicating a 3-month
        maximum.
    H OR L          Other than first letter
        High or low season
    W OR X          Other than as the first letter
        These two letters are used to state if a fare is valid on a weekday (X)
        or restricted to weekends (W).
    OW              Follows the initial booking code.
        One-way fare only
    RT              Follows the initial booking code.
        Return fare
    COUNTRY CODE    At the end of the code, except for "CH" or "IN"
        Fare bases may end with two-letter country codes. This will be the
        case when an airline has an international fare in both directions.
        For example, a fare from Great Britain to Australia may be YE3MGB, and
        YE3MAU from Australia to Great Britain. This allows the fare to have
        similar rules, but may have some variations in change fees or to
        comply with local trade restrictions.
    CH              Last two characters
        Child fare (typically up to 11 years old, but 15 in some cases)
    IN              Last two characters
        Infant fare (typically up to 2 years old, but 3 years in some cases)
    """
    abfSql = """
        UPDATE booking_fare_segments
        SET ( flight_number, board_date,
              departure_airport, arrival_airport,
              selling_class, fare_basis_code,
              valid_from_date, valid_to_date,
              update_user, update_group,
              update_time )
        = ('%s', '%s',
           '%s', '%s',
           '%s', '%s',
           '%s', '%s',
           '%s', '%s',
           NOW())
        WHERE book_no = %d
        AND fare_no = %d
        AND pax_code = '%s'""" \
        % (aFlight, aFlightDate,
           aDepart, aArrive,
           aSellClass, aFareBasis,
           aStartDate, aEndDate,
           aUser, aGroup,
           aBookNo, aFareNo, aPaxCode)
    printlog(2, "%s" % abfSql)
    cur = conn.cursor()
    printlog(2, "Updated %d row(s)" % cur.rowcount)
    if cur.rowcount > 0:
        cur.close()
        return

    printlog(1, "Add booking fare segment for booking %d:"
             " code %s flight %s date %s amount %s%d"
             % (aBookNo, aPaxCode, aFlight, aFlightDate, aCurrency, aAmount))
    abfSql = """
        INSERT INTO booking_fare_segments(
            book_no, fare_no, pax_code,
            flight_number, board_date,
            departure_airport, arrival_airport,
            selling_class, fare_basis_code,
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
           aFlight, aFlightDate,
           aDepart, aArrive,
           aSellClass, aFareBasis,
           aStartDate, aEndDate,
           aUser, aGroup)
    printlog(2, "%s" % abfSql)
    cur.execute(abfSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddBookFarePassengers(conn, aBookNo, aPaxCode, aCurrency, aAmount,
                          aUser, aGroup):
    """Add entry for booking fare passenger."""
    printlog(1, "Add booking %d fare passenger:"
             " passenger code %s amount %s%d"
             % (aBookNo, aPaxCode, aCurrency, aAmount))
    vFare = ' '
    vRestrict = ' '
    cur = conn.cursor()
    abfSql = """
        UPDATE book_fares_pass SET (
            total_amount_curr, total_amount,
            fare_construction, endrsmnt_rstrctns,
            update_user, update_group,
            update_time )
        = (
                 '%s', %f,
                 '%s', '%s',
                 '%s', '%s',
                 NOW() )
        WHERE book_no = %d
        AND pax_code = '%s'""" \
        % (aCurrency, aAmount, vFare, vRestrict,
           aUser, aGroup, aBookNo, aPaxCode)
    printlog(2, "%s" % abfSql)
    cur.execute(abfSql)
    printlog(2, "Updated %d row(s)" % cur.rowcount)
    if cur.rowcount > 0:
        cur.close()
        return

    abfSql = """
        INSERT INTO book_fares_pass(
            book_no, pax_code,
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


def AddBookFaresPayments(conn, aBookNo, aFareNo, aPaxCode, aFareBasisCode,
                         aCurrency, aAmount, aUser, aGroup, aSource=None):
    """Add entry for booking fare payment."""
    printlog(1, "Add booking %d fare %d"
             " passenger code %s payment %s%d"
             % (aBookNo, aFareNo, aPaxCode, aCurrency, aAmount))
    abfSql = """
        INSERT INTO book_fares_paym(
            book_no, fare_no, pax_code,
            payment_code, fare_calc_code,
            currency_code, fare_paymt_amt,
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
                 '%s', '%s', NOW(), %d ) """ \
        % (aBookNo, aFareNo, aPaxCode,
           aFareBasisCode,
           aCurrency, aAmount,
           aUser, aGroup, int(aSource or 0))
    printlog(2, "%s" % abfSql)
    cur = conn.cursor()
    cur.execute(abfSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddBookRequest(conn, aBookNo, aCompany, aReqCode, aReqTexts, aUser, aGroup):
    """Add booking request."""
    # Value for request sequence number
    cur = conn.cursor()
    abrSql = """SELECT MAX(rqst_sequence_no)
        FROM book_requests WHERE book_no = %d""" % aBookNo
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
                book_no, rqst_sequence_no,
                item_no, indicator, rqst_code,
                carrier_code,
                action_code, actn_number,
                processing_flag, rqr_count,
                request_text,
                all_pax_flag, all_itinerary_flag,
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


def AddPassenger(conn, aBookNo, aPaxRecs,
                 aUser, aGroup):
    """Add passenger record."""
    printlog(1, "Add passengers for booking %d: %s (%s)"
             % (aBookNo, aPaxRecs[0].passenger_name,
                aPaxRecs[0].passenger_code))
    vClientProfileNo = ' '
    vFareNo = ' '
    vTimeLimitNo = ' '
    vTtyLineNo = 0
    vTtyGrpNo = 0
    vTtyGrpSeq = 0
    cur = conn.cursor()
    for paxRec in aPaxRecs:
        apSql = """
            INSERT INTO passenger(
                book_no, pax_no, pax_name, birth_date,
                client_prfl_no, request_nos, remark_nos, fare_nos,
                contact_nos, timelmt_nos, ticket_nos, name_incl_type, pax_code,
                processing_flag, update_user, update_group, update_time,
                tty_pax_line_no, tty_pax_grp_no, tty_pax_grp_seq )
            VALUES (%d, %d,
                    '%s', '%s',
                    '%s',
                    '%s', '%s', '%s', '%s',
                    '%s', '%s', '%s',
                    '%s', '%s',
                    '%s', '%s', NOW(),
                    %d, %d, %d)""" \
            % (aBookNo, paxRec.passenger_no,
               paxRec.passenger_name, paxRec.date_of_birth,
               vClientProfileNo,
               " ", " ", vFareNo, " ",
               vTimeLimitNo, " ", " ",
               paxRec.passenger_code, paxRec.processing_flg,
               aUser, aGroup,
               vTtyLineNo, vTtyGrpNo, vTtyGrpSeq)
        printlog(2, "%s" % apSql)
        cur.execute(apSql)
        printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddContact(conn, aBookNo, aPaxRecs, aUser, aGroup):
    """Add entry for contact info."""
    cur = conn.cursor()
    for paxRec in aPaxRecs:
        printlog(1, "Add contact for booking %d: phone %s email %s"
                 % (aBookNo, paxRec.contact_phone, paxRec.contact_email))
        abfSql = """
            INSERT INTO pax_contact(
                book_no, pax_no, contact_phone_no, email_address,
                update_user, update_group, update_time )
            VALUES (
                %d, %d, '%s',
                '%s', '%s', '%s', NOW() )""" \
            % (aBookNo, paxRec.passenger_no, paxRec.contact_phone,
               paxRec.contact_email, aUser, aGroup)
        printlog(2, "%s" % abfSql)
        cur.execute(abfSql)
        printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddPayment(conn, aPaymentForm, aPaymentType, aCurrency, aAmount,
               aDocNum, aPaymentMode,
               aBookNo, aPaxName, aPaxCode,
               aBranchCode, aRemark,
               aUser, aGroup):
    """Add payment entry."""
    printlog(1, "Add booking %d payment: %s%d type %s doc %s"
             % (aBookNo, aCurrency, aAmount, aPaymentType, aDocNum))
    apSql = """
        INSERT INTO payments(
                payment_form, payment_type,
                currency_code, payment_amount,
                payment_date, document_no, payment_mode,
                book_no, pax_name, pax_code,
                origin_branch_code, remarks_text, received_from,
                paid_flag, pay_stat_flag, recpt_stat_flag, invc_stat_flag,
                status_flag,
                create_user, create_group, create_time,
                update_user, update_group, update_time)
        VALUES ('%s', '%s',
                '%s', %s,
                CURRENT_DATE, '%s', '%s',
                %d, '%s', '%s',
                '%s', '%s', ' ',
                'Y', 'A', 'A', 'A',
                'Y',
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
    printlog(2, "Pre booking %d info" % book_no)
    preBookingInfoSql = """
        SELECT bo.book_no,
            bo.pax_name_rec,
            bo.group_name,
            ( SELECT pax.pax_name
              FROM passenger AS pax
              WHERE pax.book_no=bo.book_no AND pax.passenger_no=1),
            bo.agency_code,
            bo.create_time,
            bo.status_flag,
            bo.no_of_seats,
            bo.book_category,
            ta.trade_name,
            bci.ext_book_numb,
            bo.origin_address,
            bo.scrutiny_flag,
            ( SELECT min(btl.limit_time)
              FROM book_time_limits AS btl
              WHERE btl.book_no = bo.book_no
              AND btl.timelmt_type = 'T'
              AND btl.cancel_flag = 'C'
              AND NOT EXISTS (
                    SELECT pay.book_no FROM payments AS pay
                    WHERE pay.book_no = bo.book_no
                    AND pay.paid_flag = 'Y'
                    AND pay.payment_amount > 0 ) )
        FROM bookings AS bo
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
        pax_name_rec = row[1]
        group_name = row[2]
        agency_code = row[4]
        create_time = row[5]
        status_flag = row[6]
        print("Book %d PNR %s group %s agency %s time %s status %s"
              % (book_no, pax_name_rec, group_name.strip(), agency_code,
                 create_time, status_flag))
    cur.close()


def UpdateBookPayment(conn, aBookNo, aCurrency, aPayment):
    """Update payment amount in bookings table."""
    printlog(1, "Update booking %d payment %s%f" % (aBookNo, aCurrency, aPayment))
    UbpSql = """UPDATE bookings
                SET (payment_amount, status_flag)
                  = (payment_amount+%f, 'A')
                WHERE book_no=%d""" \
             % (aPayment, aBookNo)
    printlog(2, "%s" % UbpSql)
    cur = conn.cursor()
    cur.execute(UbpSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()
