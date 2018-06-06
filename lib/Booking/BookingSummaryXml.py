# @file ReadFaresPayment.py
#

import sys
import operator
from datetime import datetime
import psycopg2  # the Informix DB module
from BarsLog import set_verbose, get_verbose, printlog

def ReadBsRetailer(conn, elBookingNumber, epcAgencyCode, v_agencyPayForm):

    if epcAgencyCode is None:
        epcAgencyCode = ''
    if v_agencyPayForm is None:
        v_agencyPayForm = ''
    print "Retailer for booking %d agency '%s' payment '%s'" \
        % (elBookingNumber, epcAgencyCode, v_agencyPayForm)
    BsRetailerSql = """
        SELECT CASE WHEN COUNT(*) > 0 THEN MAX(b.book_no) ELSE 0 END AS bn
            FROM  book AS b
            WHERE b.book_no = %d
            AND  (b.agency_code = '%s' or
                 (b.agency_code IS NULL AND b.book_no IN
                             (SELECT p.book_no
                              FROM   payments p
                              WHERE  p.payment_type = 'TP'
                              AND    p.payment_form = '%s'
                              AND    p.book_no = b.book_no)))
    """ % (elBookingNumber, epcAgencyCode, v_agencyPayForm)

    printlog(2, "%s" % BsRetailerSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(BsRetailerSql)
    n = 0
    for row in cur:
        print "\tbooking %d" % row['bn']
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsFaresPayment(conn, book_no, currency_code):

    print "Fare payments for booking %d currency %s" % (book_no, currency_code)
    FaresPaymentSql = """
SELECT fare_no,pax_code paxcode,payment_code,fare_calc_code,round(fare_paymt_amt, 2) amount,
round(fare_paymt_amt, 5) unrounded_amount,paid_curr_code currency_code,
tax_code,nation_code,refundable_flag,net_fare_flag,private_fare_flag,source_ref_id
,round( (SELECT max(nuc_rate) FROM currency_codes cc WHERE cc.currency_code = '%s') /
        coalesce( (SELECT max(nuc_rate) FROM hist_currency_codes hcc
              WHERE hcc.currency_code = bfp.paid_curr_code
              AND bfp.update_time between
              hcc.valid_from_date_time AND hcc.valid_to_date_time),
             (SELECT max(nuc_rate) FROM currency_codes cc
                WHERE cc.currency_code = bfp.paid_curr_code) ), 5 ) common_currency_factor,
(SELECT count(book_no) FROM passenger WHERE book_no = %d AND pax_code <> 'INF') pax_number
FROM book_fares_paym bfp
WHERE book_no = %d
AND payment_code <> 'FEE'
""" % (currency_code, book_no, book_no)

    printlog(2, "%s" % FaresPaymentSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(FaresPaymentSql)
    n = 0
    for row in cur:
        print "\tfare %-2s pax %-5s pay %-4s tax %2s currency factor %s count %d" \
            % (row['fare_no'], row['paxcode'], row['payment_code'], str(row['tax_code'] or ''),
               row['common_currency_factor'], row['pax_number'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsPassengerFares(conn, book_no, currency_code):

    print "Passenger fares for booking %d currency %s" % (book_no, currency_code)
    PassengerFaresSql = """
                        SELECT bfp.pax_code AS passenger_description_code,
                                bfp.total_amount_curr AS total_amount_currency,
                                round(bfp.total_amount, 2) AS total_amount,
                                round(bfp.total_amount, 5) AS unrounded_total_amount,
                                bfp.fare_construction,
                                bfp.endrsmnt_rstrctns AS endorsement_restriction,
                                round(sum(bfpm.fare_paymt_amt), 2) AS fare_amount,
                                round(sum(bfpm.fare_paymt_amt), 5) AS unrounded_fare_amount,
                                round(
                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                        WHERE cc.currency_code = '%s')
                                        /
                                        coalesce
                                        (
                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                WHERE hcc.currency_code = bfp.total_amount_curr
                                                AND bfp.update_time between
                                                hcc.valid_from_date_time AND hcc.valid_to_date_time),
                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                WHERE cc.currency_code = bfp.total_amount_curr)
                                        ), 5
                                ) AS common_currency_factor

                        FROM book_fares_pass AS bfp
                        INNER JOIN book_fares_paym AS bfpm
                        ON bfpm.book_no = bfp.book_no
                        AND bfpm.pax_code = bfp.pax_code
                        AND bfp.book_no = %d
                        GROUP BY bfp.pax_code,
                            bfp.total_amount_curr,
                            bfp.total_amount,
                            bfp.fare_construction,
                            bfp.endrsmnt_rstrctns,
                            9
                        ORDER BY bfp.pax_code
"""  % (currency_code, book_no)

    printlog(2, "%s" % PassengerFaresSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(PassengerFaresSql)
    n = 0
    for row in cur:
        print "\tpax %-5s currency factor %s amount %s" \
            % (row['passenger_description_code'],
               row['common_currency_factor'], row['total_amount'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsOldFares(conn, book_no, currency_code):

    print "Old fares for booking %d currency %s" % (book_no, currency_code)
    OldFaresSql = """
    SELECT
            bf.et_serial_no AS serial_no
            ,bf.update_time AS updated_date_time
            ,bf.fare_no
            ,bf.pax_code AS passenger_description_code
            ,bf.departure_city AS departure_city
            ,bf.arrival_airport AS arrival_city
            ,round(bf.total_amount, 2) AS total_amount
            ,round(bf.total_amount, 5) AS unrounded_total_amount
            ,bf.total_amount_curr
            ,bf.fare_stat_flag AS fare_status
            ,dcy.city_name AS departure_city_name
            ,acy.city_name AS arrival_city_name
            ,'0' AS source_reference_id
            ,coalesce(
                    (SELECT max(bfp2.refundable_flag)
                    FROM book_fares_paym AS bfp2 WHERE book_no = bf.book_no
                    AND bfp2.fare_no = bf.fare_no AND bfp2.pax_code = bf.pax_code
                    AND bfp2.payment_code = bfp.payment_code
                    AND bfp2.refundable_flag = 'N')
            ,'Y') AS refundable_flag
            ,round(coalesce(
                    (SELECT sum(bfp2.fare_paymt_amt)
                    FROM book_fares_paym AS bfp2 WHERE book_no = bf.book_no
                    AND bfp2.fare_no = bf.fare_no AND bfp2.pax_code = bf.pax_code
                    AND bfp2.payment_code = 'FEE')
            ,0), 2)                                                         AS surcharge_amount
            ,round(
                    (SELECT max(nuc_rate) FROM currency_codes AS cc
                    WHERE cc.currency_code = '%s')
                    /
                    coalesce
                    (
                            (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                            WHERE hcc.currency_code = bf.total_amount_curr
                            AND bf.update_time between
                            hcc.valid_from_date_time AND hcc.valid_to_date_time)
                    ,
                            (SELECT max(nuc_rate) FROM currency_codes AS cc
                            WHERE cc.currency_code = bf.total_amount_curr)
                    )
                    , 5
            )                                                                       AS common_currency_factor
            ,round(sum(bfp.fare_paymt_amt), 2)      AS fare_amount
            ,round(sum(bfp.fare_paymt_amt), 5)      AS unrounded_fare_amount
    FROM hist_book_fares                    AS bf
    inner join hist_book_fares_paym         AS bfp on bfp.book_no   = bf.book_no
                                                                    AND bfp.pax_code       = bf.pax_code
                                                                    AND bfp.fare_no         = bf.fare_no
                                                                    AND bfp.et_serial_no = bf.et_serial_no
                                                                    AND bf.book_no = %d
                                                                    AND bfp.payment_code IN ('FARE', 'TAX')
    left join city                          AS dcy on dcy.city_code = bf.departure_city
    left join city                          AS acy on acy.city_code = bf.arrival_airport
    group by bf.et_serial_no
                    ,bf.update_time
                    ,bf.fare_no
                    ,bf.pax_code
                    ,bf.departure_city
                    ,bf.arrival_airport
                    ,bf.total_amount
                    ,bf.total_amount_curr
                    ,bf.fare_stat_flag
                    ,dcy.city_name
                    ,acy.city_name
                ,13
                ,14
                    ,15
                    ,16
    order by bf.et_serial_no desc
                    ,bf.pax_code
                    ,bf.fare_no
""" % (currency_code, book_no)

    printlog(2, "%s" % OldFaresSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(OldFaresSql)
    n = 0
    for row in cur:
        print "\tET %s pax %-5s depart %-4s arrive %-4s amout %s" \
            % (row['serial_no'], row['passenger_description_code'], row['departure_city'], row['arrival_city'],
               row['amount'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsOldPassengerFares(conn, book_no, currency_code):

    print "Old passenger fares for booking %d currency %s" % (book_no, currency_code)
    OldPassengerFaresSql = """
                        SELECT
                                 bfp.pax_code                                          AS passenger_description_code
                                ,bfp.total_amount_curr                          AS total_amount_currency
                                ,round(bfp.total_amount, 2)                     AS total_amount
                                ,round(bfp.total_amount, 5)                     AS unrounded_total_amount
                                ,bfp.fare_construction
                                ,bfp.endrsmnt_rstrctns                          AS endorsement_restriction
                                ,round(sum(bfpm.fare_paymt_amt), 2)     AS fare_amount
                                ,round(sum(bfpm.fare_paymt_amt), 5)     AS unrounded_fare_amount
                                ,bfp.update_time AS updated_date_time
                                ,bfp.et_serial_no                                        AS serial_no

                                ,round
                                (
                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                        WHERE cc.currency_code = '%s')
                                        /
                                        coalesce
                                        (
                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                WHERE hcc.currency_code = bfp.total_amount_curr
                                                AND bfp.update_time between
                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                        ,
                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                WHERE cc.currency_code = bfp.total_amount_curr)
                                        )

                                        , 5
                                )                                                                       AS common_currency_factor


                        FROM hist_book_fares_pass               AS bfp
                        inner join hist_book_fares_paym AS bfpm  on bfpm.book_no        = bfp.book_no
                                                                                                AND bfpm.pax_code      = bfp.pax_code
                                                                                                AND bfpm.et_serial_no = bfp.et_serial_no
                                                                                                AND bfp.book_no = %d
                        group by
                                 bfp.et_serial_no
                                ,bfp.update_time
                                ,bfp.pax_code
                                ,bfp.total_amount_curr
                                ,bfp.total_amount
                                ,bfp.fare_construction
                                ,bfp.endrsmnt_rstrctns
                                ,11
                        order by
                                 bfp.et_serial_no desc
                                ,bfp.pax_code
"""  % (currency_code, book_no)

    printlog(2, "%s" % OldPassengerFaresSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(OldPassengerFaresSql)
    n = 0
    for row in cur:
        print "\tET %s pax %-5s currency factor %s amount %s" \
            % (row['serial_no'], row['passenger_description_code'],
               row['common_currency_factor'], row['total_amount'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsOldFaresPayment(conn, book_no, currency_code):

    print "Old fares payment for booking %d currency %s" % (book_no, currency_code)
    OldFaresPaymentSql = """
                        SELECT
                                 fare_no,
                                 pax_code AS passenger_description_code,
                                payment_code,
                                fare_calc_code,
                                fare_paymt_amt AS amount,
                                paid_curr_code AS currency_code,
                                tax_code,
                                nation_code,
                                refundable_flag
                                net_fare_flag,
                                private_fare_flag,
                                source_ref_id,
                                update_time AS updated_date_time,
                                et_serial_no AS serial_no,
                                ROUND(
                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                        WHERE cc.currency_code = '%s')
                                        /
                                        coalesce
                                        (
                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                WHERE hcc.currency_code = bfp.paid_curr_code
                                                AND bfp.update_time BETWEEN
                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                        ,
                                                (SELECT MAX(nuc_rate) FROM currency_codes AS cc
                                                WHERE cc.currency_code = bfp.paid_curr_code)
                                        )
                                        , 5
                                ) AS common_currency_factor
                        FROM hist_book_fares_paym AS bfp
                        WHERE book_no = %d AND payment_code <> 'FEE'
"""  % (currency_code, book_no)

    printlog(2, "%s" % OldFaresPaymentSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(OldFaresPaymentSql)
    n = 0
    for row in cur:
        print "\tET %s pax %-5s currency factor %s amount %s" \
            % (row['serial_no'], row['passenger_description_code'],
               row['common_currency_factor'], row['amount'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsStopOvers(conn, flight_number, board_date, departure_airport, arrival_airport):
    StopOversSql = """
                        SELECT fsd.arrival_airport AS stop_over_point,
                (SELECT CASE WHEN f1.departure_time > fsd.arrival_time
                                                                THEN f1.departure_time - fsd.arrival_time
                                ELSE f1.departure_time - fsd.arrival_time + 1440 end
                        FROM flight_segm_date AS f1
                        WHERE f1.flight_number = fsd.flight_number
                          AND fsd.board_date = f1.board_date
                          AND f1.leg_number > 0
                          AND f1.departure_airport = fsd.arrival_airport) AS stop_over_time
           FROM flight_segm_date AS fsd
           WHERE fsd.flight_number= '%s'
                        AND to_char(fsd.board_date, '%%d%%b%%iY') = '%s'
                        AND fsd.leg_number between (SELECT f1.leg_number
                FROM flight_segm_date AS f1
                WHERE f1.flight_number = fsd.flight_number
                 AND f1.board_date = fsd.board_date
                 AND f1.leg_number > 0
                 AND f1.departure_airport = '%s' )
                        AND (SELECT f1.leg_number
                FROM flight_segm_date AS f1
                WHERE f1.flight_number = fsd.flight_number
                 AND f1.board_date = fsd.board_date
                 AND f1.leg_number > 0
                 AND f1.arrival_airport = '%s' )
                        AND fsd.arrival_airport <> '%s'
""" % (flight_number, board_date, departure_airport, departure_airport, arrival_airport)

    printlog(2, "%s" % StopOversSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(StopOversSql)
    n = 0
    for row in cur:
        print "\t\tstop %s time %s" \
            % (row['stop_over_point'], row['stop_over_time'])
        n += 1
    if n==0:
        print "\t\t--no stops--"
    cur.close()


def ReadBsItinerary(conn, book_no):

    print "Itenary for booking %d" % (book_no)
    ItinerarySql = """SELECT
                                itn.route_no,
                                (SELECT flight_number FROM flight_shared_leg WHERE dup_flight_number = itn.flight_number AND flight_date = itn.flight_date) AS codeshareflightnumber
                                ,itn.flight_number AS flight_number
                                ,itn.selling_class
                                ,itn.flight_date AS flight_date
                                ,itn.departure_city
                                ,itn.arrival_city
                                ,substr(itn.reserve_status, 1, 2)       AS reserve_status
                                ,itn.fare_nos
                                ,departure_time
                                 ,arrival_time
                                ,ac.seat_rqst_type
                                ,itn.book_no
                                ,itn.alt_itenary_no     AS alt_itinerary_no
                                ,itn.itenary_no         AS itinerary_no
                                ,itn.departure_airport       AS departure_airport
                                ,itn.arrival_airport       AS arrival_airport
                                ,dap.airport_name       AS departure_airport_name
                                ,dcy.city_name          AS departure_city_name
                                ,aap.airport_name       AS arrival_airport_name
                                ,acy.city_name          AS arrival_city_name
                                ,itn.itenary_stat_flag
                                ,itn.request_nos
                                ,itn.date_change_ind    AS date_change_ind
                                ,case when
                                         (
                                                SELECT  coalesce(count(fsl.dup_flight_number),0)
                                                FROM    flight_shared_leg AS fsl
                                                WHERE   fsl.flight_number   = itn.flight_number
                                                        AND fsl.flight_date = itn.flight_date
                                     ) = 0
                                 then itn.flight_number
                                 else
                                     (
                                                SELECT  min(fsl.dup_flight_number)
                                                FROM    flight_shared_leg AS fsl
                                                WHERE   fsl.flight_number   = itn.flight_number
                                                        AND fsl.flight_date = itn.flight_date
                                                                AND fsl.leg_number      = 1
                                     )
                             end
                                        AS marketing_flight_number
                        FROM  itenary            AS itn
                        left join action_codes  AS ac   on action_code  = substr(itn.reserve_status, 1, 2)
                             AND ac.company_code = (SELECT company_code FROM system_param)
                        left join airport       AS dap on dap.airport_code      = itn.departure_airport
                        left join city          AS dcy on dcy.city_code         = itn.departure_city
                        left join airport       AS aap on aap.airport_code      = itn.arrival_airport
                        left join city          AS acy on acy.city_code         = itn.arrival_city
                        WHERE itn.book_no = %d
                          AND itn.itenary_stat_flag <> 'X'
                          AND (itn.flight_number like '%%OPEN' or (
                             itn.itenary_type = 'R'
                             AND ac.action_code is not null)
                          )
                        order by        itn.flight_date,
                                                itn.departure_time
"""  % (book_no)

    printlog(2, "%s" % ItinerarySql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ItinerarySql)
    n = 0
    for row in cur:
        print "\tflight %s date %s depart %s arrive %s market '%s' codeshare '%s'" \
            % (row['flight_number'], row['flight_date'], row['departure_airport'], row['arrival_airport'],
               row['marketing_flight_number'], str(row['codeshareflightnumber'] or ''))
        ReadBsStopOvers(conn, row['flight_number'], row['flight_date'], row['departure_airport'], row['arrival_airport'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsFares(conn, book_no, currency_code):

    print "Fares for booking %d currency %s" % (book_no, currency_code)
    FaresSql = """
                        SELECT
                                 bf.fare_no
                                ,bf.pax_code                                           AS passenger_description_code
                                ,bf.departure_city                                          AS departure_city
                                ,bf.arrival_airport                                            AS arrival_city
                                ,round(bf.total_amount, 2)                      AS total_amount
                                ,round(bf.total_amount, 5)                      AS unrounded_total_amount
                                ,bf.total_amount_curr                           AS total_amount_curr
                                ,bf.fare_stat_flag                                       AS fare_status
                                ,dcy.city_name                                          AS departure_city_name
                                ,acy.city_name                                          AS arrival_city_name
                                ,'0'                                                            AS source_reference_id
                                ,coalesce(
                                        (SELECT max(bfp2.refundable_flag)
                                        FROM book_fares_paym AS bfp2 WHERE book_no = bf.book_no
                                        AND bfp2.fare_no = bf.fare_no AND bfp2.pax_code = bf.pax_code
                                        AND bfp2.payment_code = bfp.payment_code
                                        AND bfp2.refundable_flag = 'N')
                                ,'Y')                                                           AS refundable_flag
                                ,round(coalesce(
                                        (SELECT sum(bfp2.fare_paymt_amt)
                                        FROM book_fares_paym AS bfp2 WHERE book_no = bf.book_no
                                        AND bfp2.fare_no = bf.fare_no AND bfp2.pax_code = bf.pax_code
                                        AND bfp2.payment_code = 'FEE')
                                ,0), 2)                                                         AS surcharge_amount
                                ,round(
                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                        WHERE cc.currency_code = '%s')
                                        /
                                        coalesce
                                        (
                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                WHERE hcc.currency_code = bf.total_amount_curr
                                                AND bf.update_time between
                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                        ,
                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                WHERE cc.currency_code = bf.total_amount_curr)
                                        )
                                , 5)                                                            AS common_currency_factor
                                ,round(sum(bfp.fare_paymt_amt), 2)      AS fare_amount
                                ,round(sum(bfp.fare_paymt_amt), 5)      AS unrounded_fare_amount
                        FROM book_fares                         AS bf
                        inner join book_fares_paym      AS bfp on bfp.book_no   = bf.book_no
                                                                                        AND bfp.pax_code       = bf.pax_code
                                                                                        AND bfp.fare_no         = bf.fare_no
                                                                                        AND bfp.payment_code IN ('FARE', 'TAX')
                                                                                        AND bf.book_no = %d
                        left join city                          AS dcy on dcy.city_code = bf.departure_city
                        left join city                          AS acy on acy.city_code = bf.arrival_airport
                        group by bf.fare_no, bf.pax_code, bf.departure_city, bf.arrival_airport
                                , bf.total_amount, bf.total_amount_curr, bf.fare_stat_flag, dcy.city_name
                                , acy.city_name, 11, 12, 13, 14
                        order by bf.pax_code, bf.fare_no
""" % (currency_code, book_no)

    printlog(2, "%s" % FaresSql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(FaresSql)
    n = 0
    for row in cur:
        print "\tpax %-5s currency factor %s amount %s" \
            % (row['passenger_description_code'],
               row['common_currency_factor'], row['total_amount'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsSummary(conn, book_no, currency_code, PaymentTypeFee='', PaymentTypeFeeTax = '', PaymentTypeFeeWaive = ''):

    print "Booking summary for booking %d currency %s" % (book_no, currency_code)
    SummarySql = """
                        SELECT
                                round(coalesce(
                                        (SELECT sum
                                                (
                                                        pa1.payment_amount *
                                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                        WHERE cc.currency_code = '%s')
                                                        /
                                                        coalesce
                                                        (
                                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                                WHERE hcc.currency_code = pa1.paid_curr_code
                                                                AND pa1.crea_date_time) between
                                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                                        ,
                                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                                WHERE cc.currency_code = pa1.paid_curr_code)
                                                        )
                                                ) FROM payments pa1
                                        WHERE pa1.book_no = bo.book_no AND pa1.paid_flag = 'Y'
                                        AND  pa1.payment_type not IN ('%s', '%s', '%s'))
                                , 0), 2) AS total_payment
                                ,round(coalesce(
                                        (SELECT sum
                                                (
                                                        bc.comm_amount *
                                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                        WHERE cc.currency_code = '%s')
                                                        /
                                                        coalesce
                                                        (
                                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                                WHERE hcc.currency_code = bc.comm_amount_curr
                                                                AND bc.update_time between
                                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                                        ,
                                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                                WHERE cc.currency_code = bc.comm_amount_curr)
                                                        )

                                                )
                                        FROM book_commission AS bc
                                        inner join passenger AS pax on pax.book_no = bc.book_no
                                                AND pax.pax_code = bc.pax_code
                                                AND bc.book_no = bo.book_no)
                                , 0), 2) AS total_comm
                                ,round(coalesce(
                                        (SELECT sum
                                                (
                                                        bfp.fare_paymt_amt *
                                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                        WHERE cc.currency_code = '%s')
                                                        /
                                                        coalesce
                                                        (
                                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                                WHERE hcc.currency_code = bfp.paid_curr_code
                                                                AND bfp.update_time between
                                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                                        ,
                                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                                WHERE cc.currency_code = bfp.paid_curr_code)
                                                        )
                                                )
                                        FROM book_fares_paym AS bfp
                                        inner join passenger AS pax on pax.book_no = bfp.book_no
                                                AND pax.pax_code = bfp.pax_code
                                                AND bfp.book_no = bo.book_no)
                                , 0), 2) AS total_fare
                                ,round(coalesce(
                                        (SELECT sum
                                                (
                                                        bfp.fare_paymt_amt *
                                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                        WHERE cc.currency_code = '%s')
                                                        /
                                                        coalesce
                                                        (
                                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                                WHERE hcc.currency_code = bfp.paid_curr_code
                                                                AND bfp.update_time between
                                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                                        ,
                                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                                WHERE cc.currency_code = bfp.paid_curr_code)
                                                        )
                                                )
                                        FROM book_fares_paym AS bfp
                                        inner join passenger AS pax on pax.book_no = bfp.book_no
                                                AND pax.pax_code = bfp.pax_code
                                                AND bfp.book_no = bo.book_no)
                                        -
                                        (SELECT sum
                                                (
                                                        pa1.payment_amount *
                                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                        WHERE cc.currency_code = '%s')
                                                        /
                                                        coalesce
                                                        (
                                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                                WHERE hcc.currency_code = pa1.paid_curr_code
                                                                AND pa1.crea_date_time between
                                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                                        ,
                                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                                WHERE cc.currency_code = pa1.paid_curr_code)
                                                        )
                                                ) FROM payments pa1
                                        WHERE pa1.book_no = bo.book_no AND pa1.paid_flag = 'Y'
                                        AND  pa1.payment_type not IN ('%s', '%s', '%s'))
                                        -
                                        (SELECT (sum
                                                (
                                                        pa.payment_amount *
                                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                        WHERE cc.currency_code = '%s')
                                                        /
                                                        coalesce
                                                        (
                                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                                WHERE hcc.currency_code = pa.paid_curr_code
                                                                AND pa.crea_date_time between
                                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                                        ,
                                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                                WHERE cc.currency_code = pa.paid_curr_code)
                                                        )
                                                )) FROM payments AS pa
                                        WHERE pa.book_no = bo.book_no
                                        AND pa.payment_type IN ('%s', '%s', '%s'))
                                , 0), 2) AS total_outstanding
                                ,round(coalesce(
                                        (SELECT sum
                                                (
                                                        bfp.fare_paymt_amt *
                                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                        WHERE cc.currency_code = '%s')
                                                        /
                                                        coalesce
                                                        (
                                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                                WHERE hcc.currency_code = bfp.paid_curr_code
                                                                AND bfp.update_time between
                                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                                        ,
                                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                                WHERE cc.currency_code = bfp.paid_curr_code)
                                                        )
                                                )
                                        FROM book_fares_paym AS bfp
                                        inner join passenger AS pax on pax.book_no = bfp.book_no
                                                AND pax.pax_code = bfp.pax_code
                                                AND bfp.payment_code = 'FEE'
                                                AND bfp.book_no = bo.book_no)
                                , 0), 2) AS total_insurance
                                ,round(coalesce(
                                        (SELECT -1 * (sum
                                                (
                                                        pa.payment_amount *
                                                        (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                        WHERE cc.currency_code = '%s')
                                                        /
                                                        coalesce
                                                        (
                                                                (SELECT max(nuc_rate) FROM hist_currency_codes AS hcc
                                                                WHERE hcc.currency_code = pa.paid_curr_code
                                                                AND pa.crea_date_time between
                                                                hcc.valid_from_date_time AND hcc.valid_to_date_time)
                                                        ,
                                                                (SELECT max(nuc_rate) FROM currency_codes AS cc
                                                                WHERE cc.currency_code = pa.paid_curr_code)
                                                                                                                                            AND bfpm.pax_code      = bfp.pax_code
                                                                                                AND bfp.book_no = %d            )
                                                )) FROM payments AS pa
                                        WHERE pa.book_no = bo.book_no
                                        AND pa.payment_type IN ('%s', '%s', '%s'))
                                , 0), 2) AS total_fee
                        FROM book AS bo WHERE bo.book_no = %s
""" % (currency_code,
       PaymentTypeFee, PaymentTypeFeeTax, PaymentTypeFeeWaive,
       currency_code,
       currency_code,
       currency_code,
       currency_code,
       PaymentTypeFee, PaymentTypeFeeTax, PaymentTypeFeeWaive,
       currency_code,
       PaymentTypeFee, PaymentTypeFeeTax, PaymentTypeFeeWaive,
       currency_code,
       currency_code,
       PaymentTypeFee, PaymentTypeFeeTax, PaymentTypeFeeWaive,
       book_no)

    printlog(2, "%s" % SummarySql)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(SummarySql)
    n = 0
    for row in cur:
        print "\t payment %s commission %s fare %s outstanding %s insurance %s fee %s" \
            % (row['total_payment'], row['total_comm'], row['total_fare'], row['total_outstanding'], row['total_insurance'], row['total_fee'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()

