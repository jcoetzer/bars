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
        select CASE WHEN COUNT(*) > 0 THEN MAX(b.book_no) ELSE 0 END as bn
            from  book as b
            where b.book_no = %d
            and  (b.book_agency_code = '%s' or
                 (b.book_agency_code is null and b.book_no in
                             (select p.book_no
                              from   payments p
                              where  p.payment_type = 'TP'
                              and    p.payment_form = '%s'
                              and    p.book_no = b.book_no)))
    """ % (elBookingNumber, epcAgencyCode, v_agencyPayForm)

    printlog("%s" % BsRetailerSql,2)

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
select fare_no,pass_code paxcode,payment_code,fare_calc_code,round(fare_paymt_amt, 2) amount,
round(fare_paymt_amt, 5) unrounded_amount,paid_curr_code currency_code,
tax_code,nation_code,refundable_flag,net_fare_flag,private_fare_flag,source_ref_id
,round( (select max(nuc_rate) from currency_codes cc where cc.currency_code = '%s') /
        nvl( (select max(nuc_rate) from hist_currency_codes hcc
              where hcc.currency_code = bfp.paid_curr_code
              and conv_inddatelong(bfp.updt_date_time) between
              hcc.valid_from_date_time and hcc.valid_to_date_time),
             (select max(nuc_rate) from currency_codes cc
                where cc.currency_code = bfp.paid_curr_code) ), 5 ) common_currency_factor,
(select count(book_no) from passenger where book_no = %d and pass_code <> 'INF') pax_number
from book_fares_paym bfp
where book_no = %d
and payment_code <> 'FEE'
""" % (currency_code, book_no, book_no)

    printlog("%s" % FaresPaymentSql,2)

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
                        select
                                 bfp.pass_code                                          as passenger_description_code
                                ,bfp.total_amount_curr                          as total_amount_currency
                                ,round(bfp.total_amount, 2)                     as total_amount
                                ,round(bfp.total_amount, 5)                     as unrounded_total_amount
                                ,bfp.fare_construction
                                ,bfp.endrsmnt_rstrctns                          as endorsement_restriction
                                ,round(sum(bfpm.fare_paymt_amt), 2)     as fare_amount
                                ,round(sum(bfpm.fare_paymt_amt), 5)     as unrounded_fare_amount

                                ,round
                                (
                                        (select max(nuc_rate) from currency_codes as cc
                                        where cc.currency_code = '%s')
                                        /
                                        nvl
                                        (
                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                where hcc.currency_code = bfp.total_amount_curr
                                                and conv_inddatelong(bfp.updt_date_time) between
                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                        ,
                                                (select max(nuc_rate) from currency_codes as cc
                                                where cc.currency_code = bfp.total_amount_curr)
                                        )

                                        , 5
                                )                                                                       as common_currency_factor

                        from book_fares_pass            as bfp
                        inner join book_fares_paym      as bfpm  on bfpm.book_no        = bfp.book_no
                                                                                                and bfpm.pass_code      = bfp.pass_code
                                                                                                and bfp.book_no = %d

                        group by
                                 bfp.pass_code
                                ,bfp.total_amount_curr
                                ,bfp.total_amount
                                ,bfp.fare_construction
                                ,bfp.endrsmnt_rstrctns
                                ,9
                        order by
                                 bfp.pass_code
"""  % (currency_code, book_no)

    printlog("%s" % PassengerFaresSql,2)

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
    select
            bf.et_serial_no                                         as serial_no
            ,conv_inddatelong(bf.updt_date_time)    as updated_date_time
            ,bf.fare_no
            ,bf.pass_code                                           as passenger_description_code
            ,bf.start_city                                          as departure_city
            ,bf.end_city                                            as arrival_city
            ,round(bf.total_amount, 2)                      as total_amount
            ,round(bf.total_amount, 5)                      as unrounded_total_amount
            ,bf.total_amount_curr
            ,bf.fare_stat_flag                                       as fare_status
            ,dcy.city_name                                          as departure_city_name
            ,acy.city_name                                          as arrival_city_name
            ,'0'                                                            as source_reference_id
            ,nvl(
                    (select max(bfp2.refundable_flag)
                    from book_fares_paym as bfp2 where book_no = bf.book_no
                    and bfp2.fare_no = bf.fare_no and bfp2.pass_code = bf.pass_code
                    and bfp2.payment_code = bfp.payment_code
                    and bfp2.refundable_flag = 'N')
            ,'Y')                                                           as refundable_flag
            ,round(nvl(
                    (select sum(bfp2.fare_paymt_amt)
                    from book_fares_paym as bfp2 where book_no = bf.book_no
                    and bfp2.fare_no = bf.fare_no and bfp2.pass_code = bf.pass_code
                    and bfp2.payment_code = 'FEE')
            ,0), 2)                                                         as surcharge_amount
            ,round
            (
                    (select max(nuc_rate) from currency_codes as cc
                    where cc.currency_code = '%s')
                    /
                    nvl
                    (
                            (select max(nuc_rate) from hist_currency_codes as hcc
                            where hcc.currency_code = bf.total_amount_curr
                            and conv_inddatelong(bf.updt_date_time) between
                            hcc.valid_from_date_time and hcc.valid_to_date_time)
                    ,
                            (select max(nuc_rate) from currency_codes as cc
                            where cc.currency_code = bf.total_amount_curr)
                    )
                    , 5
            )                                                                       as common_currency_factor
            ,round(sum(bfp.fare_paymt_amt), 2)      as fare_amount
            ,round(sum(bfp.fare_paymt_amt), 5)      as unrounded_fare_amount
    from hist_book_fares                    as bf
    inner join hist_book_fares_paym         as bfp on bfp.book_no   = bf.book_no
                                                                    and bfp.pass_code       = bf.pass_code
                                                                    and bfp.fare_no         = bf.fare_no
                                                                    and bfp.et_serial_no = bf.et_serial_no
                                                                    and bf.book_no = %d
                                                                    and bfp.payment_code in ('FARE', 'TAX')
    left join city                          as dcy on dcy.city_code = bf.start_city
    left join city                          as acy on acy.city_code = bf.end_city
    group by bf.et_serial_no
                    ,bf.updt_date_time
                    ,bf.fare_no
                    ,bf.pass_code
                    ,bf.start_city
                    ,bf.end_city
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
                    ,bf.pass_code
                    ,bf.fare_no
""" % (currency_code, book_no)

    printlog("%s" % OldFaresSql,2)

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
                        select
                                 bfp.pass_code                                          as passenger_description_code
                                ,bfp.total_amount_curr                          as total_amount_currency
                                ,round(bfp.total_amount, 2)                     as total_amount
                                ,round(bfp.total_amount, 5)                     as unrounded_total_amount
                                ,bfp.fare_construction
                                ,bfp.endrsmnt_rstrctns                          as endorsement_restriction
                                ,round(sum(bfpm.fare_paymt_amt), 2)     as fare_amount
                                ,round(sum(bfpm.fare_paymt_amt), 5)     as unrounded_fare_amount
                                ,conv_inddatelong(bfp.updt_date_time) as updated_date_time
                                ,bfp.et_serial_no                                        as serial_no

                                ,round
                                (
                                        (select max(nuc_rate) from currency_codes as cc
                                        where cc.currency_code = '%s')
                                        /
                                        nvl
                                        (
                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                where hcc.currency_code = bfp.total_amount_curr
                                                and conv_inddatelong(bfp.updt_date_time) between
                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                        ,
                                                (select max(nuc_rate) from currency_codes as cc
                                                where cc.currency_code = bfp.total_amount_curr)
                                        )

                                        , 5
                                )                                                                       as common_currency_factor


                        from hist_book_fares_pass               as bfp
                        inner join hist_book_fares_paym as bfpm  on bfpm.book_no        = bfp.book_no
                                                                                                and bfpm.pass_code      = bfp.pass_code
                                                                                                and bfpm.et_serial_no = bfp.et_serial_no
                                                                                                and bfp.book_no = %d

                        group by
                                 bfp.et_serial_no
                                ,bfp.updt_date_time
                                ,bfp.pass_code
                                ,bfp.total_amount_curr
                                ,bfp.total_amount
                                ,bfp.fare_construction
                                ,bfp.endrsmnt_rstrctns
                                ,11
                        order by
                                 bfp.et_serial_no desc
                                ,bfp.pass_code
"""  % (currency_code, book_no)

    printlog("%s" % OldPassengerFaresSql,2)

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
                        select
                                 fare_no
                                ,pass_code                                      as passenger_description_code
                                ,payment_code
                                ,fare_calc_code
                                ,round(fare_paymt_amt, 2)       as amount
                                ,round(fare_paymt_amt, 5)       as unrounded_amount
                                ,paid_curr_code                         as currency_code
                                ,tax_code
                                ,nation_code
                                ,refundable_flag
                                ,net_fare_flag
                                ,private_fare_flag
                                ,source_ref_id
                                ,conv_inddatelong(updt_date_time) as updated_date_time
                                ,et_serial_no                                    as serial_no
                                ,round
                                (
                                        (select max(nuc_rate) from currency_codes as cc
                                        where cc.currency_code = '%s')
                                        /
                                        nvl
                                        (
                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                where hcc.currency_code = bfp.paid_curr_code
                                                and conv_inddatelong(bfp.updt_date_time) between
                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                        ,
                                                (select max(nuc_rate) from currency_codes as cc
                                                where cc.currency_code = bfp.paid_curr_code)
                                        )
                                        , 5
                                ) as common_currency_factor
                        from hist_book_fares_paym as bfp
                        where book_no = %d and payment_code <> 'FEE'
"""  % (currency_code, book_no)

    printlog("%s" % OldFaresPaymentSql,2)

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
                        SELECT fsd.arrival_airport as stop_over_point,
                (select case when f1.departure_time > fsd.arrival_time
                                                                then f1.departure_time - fsd.arrival_time
                                else f1.departure_time - fsd.arrival_time + 1440 end
                        from flight_segm_date as f1
                        where f1.flight_number = fsd.flight_number
                          and fsd.board_date = f1.board_date
                          and f1.leg_number > 0
                          and f1.departure_airport = fsd.arrival_airport) as stop_over_time
           FROM flight_segm_date AS fsd
           WHERE fsd.flight_number= '%s'
                        AND to_char(fsd.board_date, '%%d%%b%%iY') = '%s'
                        and fsd.leg_number between (select f1.leg_number
                from flight_segm_date as f1
                where f1.flight_number = fsd.flight_number
                 and f1.board_date = fsd.board_date
                 and f1.leg_number > 0
                 and f1.departure_airport = '%s' )
                        and (select f1.leg_number
                from flight_segm_date as f1
                where f1.flight_number = fsd.flight_number
                 and f1.board_date = fsd.board_date
                 and f1.leg_number > 0
                 and f1.arrival_airport = '%s' )
                        and fsd.arrival_airport <> '%s'
""" % (flight_number, board_date, departure_airport, departure_airport, arrival_airport)

    printlog("%s" % StopOversSql,2)

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
    ItinerarySql = """
                        select
                                itn.route_no
                                ,(select flight_number from flight_shared_leg where dup_flight_number = itn.flight_number and flight_date = itn.flight_date) as codeshareflightnumber
                                ,itn.flight_number
                                ,itn.selling_class
                                ,to_char(itn.flight_date,'%%d%%b%%iY')     as flight_date
                                ,itn.departure_city
                                ,itn.arrival_city
                                ,substr(itn.reserve_status, 1, 2)       as reserve_status
                                ,itn.fare_nos
                                ,substr(case when departure_time / 60 < 10 then '0' else '' end || departure_time / 60::char(2), 1, 2) || ':' ||
                 substr('0' || mod(departure_time, 60), length(mod(departure_time, 60)::char(2)), 2)   as departure_time
                                 ,substr(case when arrival_time / 60 < 10 then '0' else '' end || arrival_time / 60::char(2), 1, 2) || ':' ||
                 substr('0' || mod(arrival_time, 60), length(mod(arrival_time, 60)::char(2)), 2)       as arrival_time
                                ,ac.seat_rqst_type
                                ,itn.book_no
                                ,itn.alt_itenary_no     as alt_itinerary_no
                                ,itn.itenary_no         as itinerary_no
                                ,itn.departure_airport       as departure_airport_code
                                ,itn.arrival_airport       as arrival_airport_code
                                ,dap.airport_name       as departure_airport_name
                                ,dcy.city_name          as departure_city_name
                                ,aap.airport_name       as arrival_airport_name
                                ,acy.city_name          as arrival_city_name
                                ,itn.itenary_stat_flag
                                ,itn.request_nos
                                ,itn.date_change_ind    as date_change_ind
                                ,case when
                                         (
                                                select  nvl(count(fsl.dup_flight_number),0)
                                                from    flight_shared_leg as fsl
                                                where   fsl.flight_number   = itn.flight_number
                                                        and fsl.flight_date = itn.flight_date
                                     ) = 0
                                 then itn.flight_number
                                 else
                                     (
                                                select  min(fsl.dup_flight_number)
                                                from    flight_shared_leg as fsl
                                                where   fsl.flight_number   = itn.flight_number
                                                        and fsl.flight_date = itn.flight_date
                                                                and fsl.leg_number      = 1
                                     )
                             end
                                        as marketing_flight_number
                        from  itenary            as itn
                        left join action_codes  as ac   on action_code  = substr(itn.reserve_status, 1, 2)
                                                                                                                                  and ac.company_code = (select company_code from system_param)
                        left join airport       as dap on dap.airport_code      = itn.departure_airport
                        left join city          as dcy on dcy.city_code         = itn.departure_city
                        left join airport       as aap on aap.airport_code      = itn.arrival_airport
                        left join city          as acy on acy.city_code         = itn.arrival_city
                        where itn.book_no = %d
                          and itn.itenary_stat_flag <> 'X'
                          and (itn.flight_number like '%%OPEN' or (
                             itn.itenary_type = 'R'
                             and ac.action_code is not null)
                          )
                        order by        itn.flight_date,
                                                itn.departure_time
"""  % (book_no)

    printlog("%s" % ItinerarySql,2)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Run query
    cur.execute(ItinerarySql)
    n = 0
    for row in cur:
        print "\tflight %s date %s depart %s arrive %s market '%s' codeshare '%s'" \
            % (row['flight_number'], row['flight_date'], row['departure_airport_code'], row['arrival_airport_code'],
               row['marketing_flight_number'], str(row['codeshareflightnumber'] or ''))
        ReadBsStopOvers(conn, row['flight_number'], row['flight_date'], row['departure_airport_code'], row['arrival_airport_code'])
        n += 1
    if n==0:
        print "\t--none--"
    cur.close()


def ReadBsFares(conn, book_no, currency_code):

    print "Fares for booking %d currency %s" % (book_no, currency_code)
    FaresSql = """
                        select
                                 bf.fare_no
                                ,bf.pass_code                                           as passenger_description_code
                                ,bf.start_city                                          as departure_city
                                ,bf.end_city                                            as arrival_city
                                ,round(bf.total_amount, 2)                      as total_amount
                                ,round(bf.total_amount, 5)                      as unrounded_total_amount
                                ,bf.total_amount_curr                           as total_amount_curr
                                ,bf.fare_stat_flag                                       as fare_status
                                ,dcy.city_name                                          as departure_city_name
                                ,acy.city_name                                          as arrival_city_name
                                ,'0'                                                            as source_reference_id
                                ,nvl(
                                        (select max(bfp2.refundable_flag)
                                        from book_fares_paym as bfp2 where book_no = bf.book_no
                                        and bfp2.fare_no = bf.fare_no and bfp2.pass_code = bf.pass_code
                                        and bfp2.payment_code = bfp.payment_code
                                        and bfp2.refundable_flag = 'N')
                                ,'Y')                                                           as refundable_flag
                                ,round(nvl(
                                        (select sum(bfp2.fare_paymt_amt)
                                        from book_fares_paym as bfp2 where book_no = bf.book_no
                                        and bfp2.fare_no = bf.fare_no and bfp2.pass_code = bf.pass_code
                                        and bfp2.payment_code = 'FEE')
                                ,0), 2)                                                         as surcharge_amount
                                ,round(
                                        (select max(nuc_rate) from currency_codes as cc
                                        where cc.currency_code = '%s')
                                        /
                                        nvl
                                        (
                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                where hcc.currency_code = bf.total_amount_curr
                                                and conv_inddatelong(bf.updt_date_time) between
                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                        ,
                                                (select max(nuc_rate) from currency_codes as cc
                                                where cc.currency_code = bf.total_amount_curr)
                                        )
                                , 5)                                                            as common_currency_factor
                                ,round(sum(bfp.fare_paymt_amt), 2)      as fare_amount
                                ,round(sum(bfp.fare_paymt_amt), 5)      as unrounded_fare_amount
                        from book_fares                         as bf
                        inner join book_fares_paym      as bfp on bfp.book_no   = bf.book_no
                                                                                        and bfp.pass_code       = bf.pass_code
                                                                                        and bfp.fare_no         = bf.fare_no
                                                                                        and bfp.payment_code in ('FARE', 'TAX')
                                                                                        and bf.book_no = %d
                        left join city                          as dcy on dcy.city_code = bf.start_city
                        left join city                          as acy on acy.city_code = bf.end_city
                        group by bf.fare_no, bf.pass_code, bf.start_city, bf.end_city
                                , bf.total_amount, bf.total_amount_curr, bf.fare_stat_flag, dcy.city_name
                                , acy.city_name, 11, 12, 13, 14
                        order by bf.pass_code, bf.fare_no
""" % (currency_code, book_no)

    printlog("%s" % FaresSql,2)

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
                        select
                                round(nvl(
                                        (select sum
                                                (
                                                        pa1.payment_amount *
                                                        (select max(nuc_rate) from currency_codes as cc
                                                        where cc.currency_code = '%s')
                                                        /
                                                        nvl
                                                        (
                                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                                where hcc.currency_code = pa1.paid_curr_code
                                                                and conv_inddatelong(pa1.crea_date_time) between
                                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                                        ,
                                                                (select max(nuc_rate) from currency_codes as cc
                                                                where cc.currency_code = pa1.paid_curr_code)
                                                        )
                                                ) from payments pa1
                                        where pa1.book_no = bo.book_no and pa1.paid_flag = 'Y'
                                        and  pa1.payment_type not in ('%s', '%s', '%s'))
                                , 0), 2)                                                                        as total_payment

                                ,round(nvl(
                                        (select sum
                                                (
                                                        bc.comm_amount *
                                                        (select max(nuc_rate) from currency_codes as cc
                                                        where cc.currency_code = '%s')
                                                        /
                                                        nvl
                                                        (
                                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                                where hcc.currency_code = bc.comm_amount_curr
                                                                and conv_inddatelong(bc.updt_date_time) between
                                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                                        ,
                                                                (select max(nuc_rate) from currency_codes as cc
                                                                where cc.currency_code = bc.comm_amount_curr)
                                                        )

                                                )
                                        from book_commission as bc
                                        inner join passenger as pax on pax.book_no = bc.book_no
                                                and pax.pass_code = bc.pass_code
                                                and bc.book_no = bo.book_no)
                                , 0), 2)                                                                        as total_comm

                                ,round(nvl(
                                        (select sum
                                                (
                                                        bfp.fare_paymt_amt *
                                                        (select max(nuc_rate) from currency_codes as cc
                                                        where cc.currency_code = '%s')
                                                        /
                                                        nvl
                                                        (
                                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                                where hcc.currency_code = bfp.paid_curr_code
                                                                and conv_inddatelong(bfp.updt_date_time) between
                                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                                        ,
                                                                (select max(nuc_rate) from currency_codes as cc
                                                                where cc.currency_code = bfp.paid_curr_code)
                                                        )
                                                )
                                        from book_fares_paym as bfp
                                        inner join passenger as pax on pax.book_no = bfp.book_no
                                                and pax.pass_code = bfp.pass_code
                                                and bfp.book_no = bo.book_no)
                                , 0), 2)
                                                                                                                        as total_fare
                                ,round(nvl(
                                        (select sum
                                                (
                                                        bfp.fare_paymt_amt *
                                                        (select max(nuc_rate) from currency_codes as cc
                                                        where cc.currency_code = '%s')
                                                        /
                                                        nvl
                                                        (
                                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                                where hcc.currency_code = bfp.paid_curr_code
                                                                and conv_inddatelong(bfp.updt_date_time) between
                                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                                        ,
                                                                (select max(nuc_rate) from currency_codes as cc
                                                                where cc.currency_code = bfp.paid_curr_code)
                                                        )
                                                )
                                        from book_fares_paym as bfp
                                        inner join passenger as pax on pax.book_no = bfp.book_no
                                                and pax.pass_code = bfp.pass_code
                                                and bfp.book_no = bo.book_no)
                                        -
                                        (select sum
                                                (
                                                        pa1.payment_amount *
                                                        (select max(nuc_rate) from currency_codes as cc
                                                        where cc.currency_code = '%s')
                                                        /
                                                        nvl
                                                        (
                                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                                where hcc.currency_code = pa1.paid_curr_code
                                                                and conv_inddatelong(pa1.crea_date_time) between
                                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                                        ,
                                                                (select max(nuc_rate) from currency_codes as cc
                                                                where cc.currency_code = pa1.paid_curr_code)
                                                        )
                                                ) from payments pa1
                                        where pa1.book_no = bo.book_no and pa1.paid_flag = 'Y'
                                        and  pa1.payment_type not in ('%s', '%s', '%s'))
                                        -
                                        (select (sum
                                                (
                                                        pa.payment_amount *
                                                        (select max(nuc_rate) from currency_codes as cc
                                                        where cc.currency_code = '%s')
                                                        /
                                                        nvl
                                                        (
                                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                                where hcc.currency_code = pa.paid_curr_code
                                                                and conv_inddatelong(pa.crea_date_time) between
                                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                                        ,
                                                                (select max(nuc_rate) from currency_codes as cc
                                                                where cc.currency_code = pa.paid_curr_code)
                                                        )
                                                )) from payments as pa
                                        where pa.book_no = bo.book_no
                                        and pa.payment_type in ('%s', '%s', '%s'))
                                , 0), 2)                                                                        as total_outstanding
                                ,round(nvl(
                                        (select sum
                                                (
                                                        bfp.fare_paymt_amt *
                                                        (select max(nuc_rate) from currency_codes as cc
                                                        where cc.currency_code = '%s')
                                                        /
                                                        nvl
                                                        (
                                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                                where hcc.currency_code = bfp.paid_curr_code
                                                                and conv_inddatelong(bfp.updt_date_time) between
                                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                                        ,
                                                                (select max(nuc_rate) from currency_codes as cc
                                                                where cc.currency_code = bfp.paid_curr_code)
                                                        )
                                                )
                                        from book_fares_paym as bfp
                                        inner join passenger as pax on pax.book_no = bfp.book_no
                                                and pax.pass_code = bfp.pass_code
                                                and bfp.payment_code = 'FEE'
                                                and bfp.book_no = bo.book_no)
                                , 0), 2)                                                                        as total_insurance
                                ,round(nvl(
                                        (select -1 * (sum
                                                (
                                                        pa.payment_amount *
                                                        (select max(nuc_rate) from currency_codes as cc
                                                        where cc.currency_code = '%s')
                                                        /
                                                        nvl
                                                        (
                                                                (select max(nuc_rate) from hist_currency_codes as hcc
                                                                where hcc.currency_code = pa.paid_curr_code
                                                                and conv_inddatelong(pa.crea_date_time) between
                                                                hcc.valid_from_date_time and hcc.valid_to_date_time)
                                                        ,
                                                                (select max(nuc_rate) from currency_codes as cc
                                                                where cc.currency_code = pa.paid_curr_code)
                                                        )
                                                )) from payments as pa
                                        where pa.book_no = bo.book_no
                                        and pa.payment_type in ('%s', '%s', '%s'))
                                , 0), 2)                                                                        as total_fee
                        from book as bo where bo.book_no = %s
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

    printlog("%s" % SummarySql,2)

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

