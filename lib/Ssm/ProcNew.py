# @file ProcNew.py
#

import sys
import ply.lex as lex
import ply.yacc as yacc

from SsmData import SsmData, read_ssm_data
from SsmDb import GetConfigTableNo, CheckCityPair
from BarsLog import printlog, set_verbose
from ReadDateTime import ReadDate, DateRange
import datetime


def CheckAircraftConfig(conn, acft_code):
    ConfigTableNo = None
    caSql = "SELECT config_table_no FROM aircraft_config WHERE aircraft_code = '%s' LIMIT 1" % acft_code
    cur = conn.cursor()
    printlog(2, "%s" % caSql)
    cur.execute(caSql)
    spn = 0
    for row in cur:
        ConfigTableNo = row[0]
    cur.close()
    return ConfigTableNo


def FpFromSsm(conn, flightNumber, startDate, endDate, frequencyCode, userName, groupName):

    spnSql = "SELECT COALESCE(MAX(schedule_period_no),0) FROM flight_periods"
    cur = conn.cursor()
    printlog(2, "%s" % spnSql)
    cur.execute(spnSql)
    spn = 0
    for row in cur:
        spn = int(row[0])

    spn += 1
    printlog(1, "New schedule period %d" % spn)

    cur.close()
    return spn


def FpLegsFromSsm(conn, flightNumber, schedPerdNo,
                  depAirport, depTerminal, depTime,
                  arrAirport, arrTerminal, arrTime,
                  flightPath, configNo, legNo):

    cur = conn.cursor()
    fplSql = "SELECT s1.nation_code, s2.nation_code " \
            "FROM state s1, city c1, airport a1, state s2, city c2, airport a2 " \
            "WHERE a1.airport_code = '%s' " \
            "AND a1.city_code = c1.city_code " \
            "AND c1.state_code = s1.state_code " \
            "AND a2.airport_code = '%s' " \
            "AND a2.city_code = c2.city_code " \
            "AND c2.state_code = s2.state_code" % \
                (depAirport, arrAirport)
    printlog(2, "%s" % fplSql)
    cur.execute(fplSql)
    spn = 0
    depAirport = ''
    arrAirport = ''
    for row in cur:
        depNation = row[0]
        arrNation = row[1]
        print "From %s [%s] to %s [%s]" % (depAirport, row[0], arrAirport)

    fplSql = "INSERT INTO flight_perd_legs ( " \
        "flight_number, schedule_period_no, " \
        "departure_airport, arrival_airport, departure_time, arrival_time, " \
        "date_change_ind, config_table_no, flight_path_code, " \
        "departure_terminal, arrival_terminal, leg_number, " \
        "user_name, user_group, update_time ) " \
        "VALUES ( '%s', %d, " \
                 "'%s', '%s', '%s', '%s'," \
                 "%d, '%s', '%s'," \
                 "'%s', '%s', %d," \
                 "'%s', '%s', NOW() )" % \
            ( flightNumber, schedPerdNo,
              depAirport, arrAirport, depTime, arrTime,
              0, configNo, flightPath,
              depTerminal, arrTerminal, legNo,
              'SSM', 'SSM' )
    printlog(2, "%s" % fplSql)
    cur.execute(fplSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddFlightSegmDate(conn,
                      aflight_number,
                      assm_tmp_date2,
                      acity_pair,
                      assm_tmp_date,
                      adeparture_airport,
                      aarrival_airport,
                      adeparture_time,
                      aarrival_time,
                      adate_change_ind,
                      aflight_path_code,
                      adeparture_terminal,
                      aarrival_terminal,
                      aflgt_sched_status,
                      aaircraft_code,
                      aflight_closed_flag,
                      aflight_brdng_flag,
                      ano_of_stops,
                      aleg_number,
                      asegment_number,
                      aschedule_period_no):
    cur = conn.cursor()
    fsdSql = "INSERT INTO flight_segm_date (" \
        "flight_number, board_date," \
        "city_pair, flight_date," \
        "departure_airport, arrival_airport," \
        "departure_time, arrival_time," \
        "date_change_ind, flight_path_code," \
        "departure_terminal, arrival_terminal," \
        "flgt_sched_status, aircraft_code," \
        "flight_closed_flag, flight_brdng_flag," \
        "no_of_stops, leg_number," \
        "segment_number,  schedule_period_no, user_name, user_group, update_time) " \
        "VALUES ('%s', '%s', " \
        "%d, '%s', " \
        "'%s', '%s', " \
        "'%s', '%s'," \
        "'%s', '%s', " \
        "'%s', '%s', " \
        "'%s', '%s'," \
        " '%s', '%s', " \
        "%d, %d, " \
        "%d, %d, 'SSM','SSM', NOW() )" \
        % (aflight_number, assm_tmp_date2,
           acity_pair, assm_tmp_date,
           adeparture_airport, aarrival_airport,
           adeparture_time, aarrival_time,
           adate_change_ind, aflight_path_code,
           adeparture_terminal, aarrival_terminal,
           aflgt_sched_status, aaircraft_code,
           aflight_closed_flag, aflight_brdng_flag,
           ano_of_stops, aleg_number,
           asegment_number, aschedule_period_no)
    printlog(2, "%s" % fsdSql)
    cur.execute(fsdSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddFlightPeriodLegs(conn,
                        aflight_number,
                        aschedule_period_no,
                        adeparture_airport,
                        aarrival_airport,
                        adeparture_time,
                        aarrival_time,
                        adate_change_ind,
                        aconfig_table_no,
                        aflight_path_code,
                        adeparture_terminal,
                        aarrival_terminal,
                        aleg_number):
    """Add flight period legs."""
    cur = conn.cursor()
    fplSql = """
    INSERT INTO flight_perd_legs (
        flight_number, schedule_period_no, departure_airport,
        arrival_airport, departure_time, arrival_time,
        date_change_ind, config_table_no,
        flight_path_code, departure_terminal,
        arrival_terminal, leg_number,
        user_name, user_group, update_time )
    VALUES (
        '%s',%d,'%s','%s','%s','%s',%d,'%s','%s','%s','%s',%d,'SSM','SSM',NOW())""" \
    % (aflight_number, aschedule_period_no, adeparture_airport,
       aarrival_airport, adeparture_time, aarrival_time,
       adate_change_ind, aconfig_table_no,
       aflight_path_code, adeparture_terminal,
       aarrival_terminal, aleg_number)
    printlog(2, "%s" % fplSql)
    cur.execute(fplSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddFlightPeriodSegment(conn,
                           aflight_number,
                           aschedule_period_no,
                           acity_pair,
                           aaircraft_code,
                           apost_control_flag,
                           asegment_number):
    cur = conn.cursor()
    fplSql = \
        "INSERT INTO flight_perd_segm (" \
        "flight_number, schedule_period_no, city_pair, post_control_flag," \
        "aircraft_code, flight_closed_flag, flight_brdng_flag," \
        "segment_number, update_time ) " \
        "VALUES ( '%s', %d, %d, '%s'," \
        "'%s', 'N', 'N'," \
        "%d, NOW() )" \
        % (aflight_number, aschedule_period_no, acity_pair,
           apost_control_flag,
           aaircraft_code,
           asegment_number)
    printlog(2, "%s" % fplSql)
    cur.execute(fplSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def IsPeriodToBeExtended(conn, startDate, endDate, startDateMinusOne,
                         frequency_codes, flightNumber, aircraftConfig):
    alteredFrequency = ""
    d = 1
    while d <= 7:
        if d in frequency_codes:
            alteredFrequency += "%d" % d
        else:
            alteredFrequency += "-"
        d += 1
    print "Frequency %s" % alteredFrequency
    spnSql = "SELECT fsd.schedule_period_no" \
        " FROM flight_periods fp,flight_segm_date fsd,flight_perd_legs fpl" \
        " GROUP BY fp.flight_number, fp.start_date,fp.end_date," \
        "fp.frequency_code, fp.schedule_period_no," \
        "fp.flgt_sched_status, fsd.flight_number," \
        "fsd.flight_date, fsd.flgt_sched_status," \
        "fsd.schedule_period_no, fp.via_cities," \
        "fpl.flight_number , fpl.schedule_period_no," \
        "fpl.config_table_no" \
        " HAVING fp.end_date = MAX ( fp.end_date )" \
        " AND end_date <= '%s'" \
        " AND '%s' NOT BETWEEN fp.start_date AND fp.end_date" \
        " AND '%s' NOT BETWEEN fp.start_date AND fp.end_date" \
        " AND fp.flight_number = fsd.flight_number" \
        " AND fpl.flight_number = fsd.flight_number" \
        " AND fp.schedule_period_no = fsd.schedule_period_no" \
        " AND fpl.schedule_period_no = fsd.schedule_period_no" \
        " AND fp.flgt_sched_status = fsd.flgt_sched_status" \
        " AND fsd.flight_date NOT BETWEEN '%s' AND '%s'" \
        " AND ( SELECT COUNT(flight_date) FROM flight_segm_date WHERE flight_date BETWEEN '%s' AND '%s' AND flight_number = fp.flight_number ) = 0" \
        " AND fp.end_date + 7 > '%s'" \
        " AND fp.flgt_sched_status IN ( 'A', 'S' )" \
        " AND fp.flight_number = '%s'" \
        " AND fpl.config_table_no = '%s'" % (
        startDateMinusOne,
        startDate, endDate,
        startDate, endDate,
        startDate, endDate,
        startDate,
        flightNumber, aircraftConfig )
        #" AND ( WEEKDAY ( '%s' ))::CHAR IN ('%c', '%c', '%c', '%c', '%c', '%c', '%c' )" \
        #alteredFrequency[0:1],
        #alteredFrequency[1:2],
        #alteredFrequency[2:3],
        #alteredFrequency[3:4],
        #alteredFrequency[4:5],
        #alteredFrequency[5:6],
        #alteredFrequency[6:7],
        #" AND fp.frequency_code = '%s'"freqCode \
        #" AND fp.via_cities = '%s'" newViacities\

    cur = conn.cursor()
    printlog(2, "%s" % spnSql)
    cur.execute(spnSql)

    spn = 0
    for row in cur:
        spn = int(row[0])

    print "Schedule period %d" % spn
    cur.close()
    return spn


def WriteFlightInfo(conn,
                    flight,
                    boardDate,
                    seqNo,
                    adeparture_time,
                    aarrival_time,
                    adeparture_airport,
                    aarrival_airport,
                    aDelayCode,
                    aRemarks,
                    aTailNumber,
                    aDescription,
                    userName,
                    groupName):
    cur = conn.cursor()
    fiSql = "INSERT INTO flight_information (" \
        " flight_number, board_date," \
        " departure_airport, arrival_airport," \
        " seq_no, delay_code," \
        " delay_description, etd_time," \
        " eta_time, tail_number, remarks," \
        " user_name, user_group, update_time )" \
        " VALUES ( '%s', '%s'," \
                  "'%s', '%s'," \
                  " %d, '%s', '%s', " \
                  "'%s', '%s', " \
                  "'%s', '%s'," \
                  "'%s', '%s', NOW() )" % \
            (flight, boardDate,
             adeparture_airport, aarrival_airport,
             seqNo, aDelayCode, aDescription,
             adeparture_time, aarrival_time,
             aTailNumber, aRemarks,
             userName, groupName)
    printlog(2, "%s" % fiSql)
    cur.execute(fiSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddFlightPeriod(conn,
                    pflight_number,
                    departure_airport,
                    arrival_airport,
                    start_date,
                    end_date,
                    pfrequency_code,
                    vschedule_period_no,
                    iend_date,
                    puser_name,
                    puser_group):
    """Add flight period."""
    cur = conn.cursor()
    fpSql = "INSERT INTO flight_periods(" \
            "flight_number, start_date, end_date, frequency_code," \
            "schedule_period_no, invt_end_date, " \
            "control_branch, invt_control_flag, wait_lst_ctrl_flag, via_cities, " \
            "flgt_sched_status, open_end_flag, scrutiny_flag, gen_flag_invt, " \
            "user_name, user_group, update_time) " \
            "VALUES(" \
            "'%s', '%s', '%s', '%s', " \
            "%d, '%s'," \
            "' ', ' ', ' ', '%s#%s', " \
            "'A', 'N', 'N', 'N'," \
            "'%s', '%s', NOW() )" \
        % (pflight_number, start_date, end_date, pfrequency_code,
           vschedule_period_no, end_date,
           departure_airport, arrival_airport,
           puser_name, puser_group)
    printlog(2, "%s" % fpSql)
    cur.execute(fpSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddFlightSharedLeg(conn, flight_number, flight_date, spn,
                       departure_city, arrival_city,
                       departure_time, arrival_time):
    """Add codeshare data."""
    fslSql = """
    INSERT INTO flight_shared_leg(
        dup_flight_number, dup_board_date, dup_departure_airport, dup_arrival_airport,
        dup_flight_date, flight_number, schedule_period_no, board_date, flight_date,
        departure_airport, arrival_airport, departure_time, arrival_time,
        date_change_ind, flight_path_code, departure_terminal, arrival_terminal,
        config_table_no, aircraft_code, leg_number, update_user, update_time )
     VALUES (
        '%s', '%s', '%s', '%s',
        '%s', '%s', %d, '%s', '%s', '%s',
        'N', ' ', '-', '-',
        '%s', '%s', 1, '%s', CURRENT_TIMESTAMP )""" \
    % (flight_number, flight_date, departure_city, arrival_city,
       flight_date, flight_number, spn,  flight_date, flight_date,
       departure_city, arrival_city, departure_time, arrival_time,
       airport_code, airport_code, user_name)


def AddInventorySegment(conn, pflight_number, vflight_date,
                        tcity_pair, vselling_class,
                        vdeparture_city, varrival_city,
                        vleg_number, vsegment_number, vob_profile_no,
                        vgroup_seat_lvl, vseat_protect_lvl, vlimit_sale_lvl,
                        voverbooking_lvl, vposting_lvl,
                        vsale_notify_lvl, vcancel_notify_lvl, vseat_capacity,
                        vsegm_closed_flag, vwl_closed_flag,
                        vwl_clr_inhbt_flag, vwl_rel_prty_flag,
                        vdisplay_priority, pschedule_period_no,
                        pupdt_user_code, pupdt_dest_id):
    """Add inventory segment."""
    isSql = "INSERT INTO inventry_segment" \
            "( flight_number, flight_date," \
            "city_pair, selling_class, departure_city, arrival_city," \
            "leg_number, segment_number, ob_profile_no, " \
            "group_seat_lvl,seat_protect_lvl,limit_sale_lvl,overbooking_lvl,posting_lvl," \
            "sale_notify_lvl,cancel_notify_lvl,seat_capacity," \
            "overbooking_percnt," \
            "nett_sngl_sold," \
            "nett_sngl_wait," \
            "nett_group_sold," \
            "nett_group_wait," \
            "nett_nrev_sold," \
            "nett_nrev_wait," \
            "segm_sngl_sold," \
            "segm_sngl_wait," \
            "segm_group_sold," \
            "segm_group_wait," \
            "segm_nrev_sold," \
            "segm_nrev_wait," \
            "segm_group_nrealsd," \
            "segm_sngl_ticktd," \
            "segm_group_ticktd," \
            "segm_nrev_ticktd," \
            "segment_closed_flag,wl_closed_flag, wl_clr_inhibit_flag,wl_rel_prty_flag," \
            "scrutiny_flag, display_priority,schedule_period_no," \
            "invt_updt_flag, user_name, group_name, update_time )" \
            " VALUES ( '%s', '%s'," \
            " %d, '%s', '%s', '%s'," \
            " %d, '%s', '%s', " \
            " %d, %d, %d, %d, %d," \
            " %d, %d, %d," \
            " 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0," \
            " '%s', '%s', '%s', '%s'," \
            " 'N', %d, %d," \
            " 'N', '%s', '%s', NOW() )" \
            % (pflight_number, vflight_date.strftime("%Y-%m-%d"),
               tcity_pair, vselling_class, vdeparture_city, varrival_city,
               vleg_number, vsegment_number, vob_profile_no,
               vgroup_seat_lvl, vseat_protect_lvl, vlimit_sale_lvl, voverbooking_lvl, vposting_lvl,
               vsale_notify_lvl, vcancel_notify_lvl, vseat_capacity,
               vsegm_closed_flag, vwl_closed_flag, vwl_clr_inhbt_flag, vwl_rel_prty_flag,
               vdisplay_priority, pschedule_period_no,
               pupdt_user_code, pupdt_dest_id)
    printlog(2, "%s" % isSql)
    cur = conn.cursor()
    cur.execute(isSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddFlightDateLeg(conn,
                     flight,
                     boardDate,
                     legNo,
                     adeparture_time,
                     adeparture_airport,
                     aarrival_airport,
                     userName,
                     groupName):
    """Add flight date leg."""
    fdlSql = """
        INSERT INTO flight_date_leg (
            flight_number, board_date, flight_date, departure_time,
            departure_airport, arrival_airport, leg_number,
            update_user, update_group, update_time )
        VALUES (
            '%s', '%s', '%s', '%s',
            '%s', '%s', %d,
            '%s', '%s', NOW() )""" \
        % (flight, boardDate, boardDate, adeparture_time,
           adeparture_airport, aarrival_airport, legNo,
           userName, groupName)
    printlog(2, "%s" % fdlSql)
    cur = conn.cursor()
    cur.execute(fdlSql)
    printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddFlightPeriodClasses(conn, flightNumber, spn, class_codes):
    """Add classes for flight period."""
    cur = conn.cursor()
    dp = 0

    for class_code in class_codes:
        lc = len(class_code)
        i = lc - 1
        while i > 0:
            dp += 1
            fpcSql = """
            INSERT INTO flight_perd_cls(
                flight_number, schedule_period_no, selling_class,
                parent_sell_cls, display_priority, update_time )
            VALUES (
                '%s', %d, '%s',
                '%s', %d, NOW() )""" \
            % (flightNumber, spn, class_code[i], class_code[i-1],  # class_code[0:i],
               dp)
            printlog(2, "%s" % fpcSql)
            cur.execute(fpcSql)
            printlog(2, "Inserted %d row(s)" % cur.rowcount)
            i -= 1
        dp += 1
        fpcSql = """
        INSERT INTO flight_perd_cls(
            flight_number, schedule_period_no, selling_class, parent_sell_cls,
            display_priority, update_time )
        VALUES (
            '%s', %d, '%s', '%s',
            %d, NOW() )""" \
        % (flightNumber, spn, class_code[0], class_code[0],
           dp)
        printlog(2, "%s" % fpcSql)
        cur.execute(fpcSql)
        printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddFlightPeriodSegmentClasses(conn, flight_number, spn, city_pair,
                                  class_codes, configs):
    """Add flight period segment classes."""
    cur = conn.cursor()
    i = 0
    printlog(1, "Add flight period segment classes %s" % configs)
    for class_code in class_codes:
        lc = len(class_code)
        j = 0
        while j < lc:
            fpscSql = """
            INSERT INTO flt_perd_seg_cls(
                    flight_number, schedule_period_no, city_pair, selling_class,
                    group_seat_lvl, seat_protect_lvl, limit_sale_lvl, overbooking_lvl,
                    posting_lvl, sale_notify_lvl, cancel_notify_lvl,
                    seat_capacity,
                    ob_profile_no, segment_closed_flag, wl_closed_flag, wl_clr_inhibit_flag,
                    wl_rel_prty_flag, segment_number, update_time)
                VALUES (
                    '%s', %d, %d, '%s',
                    0, 0, 0, 0,
                    0, 0, 0,
                    %d,
                    '', 'N', 'N', 'N',
                    'N', 1, NOW() )""" \
            % (flight_number, spn, city_pair, class_code[j],
               int(configs[i]))
            printlog(2, "%s" % fpscSql)
            cur.execute(fpscSql)
            printlog(2, "Inserted %d row(s)" % cur.rowcount)
            j += 1
        i += 1
    cur.close()


def AddFlightPeriodParents(conn, flight_number, spn, class_codes):
    """Add flight period class parents."""
    printlog(2, "Add parents for flight %s classes %s (%d)"
             % (flight_number, class_codes, spn))
    cur = conn.cursor()
    for class_code in class_codes:
        lc = len(class_code)
        i = lc - 1
        printlog(2, "Add parents for classes %s (%d)" % (class_code, lc))
        while i > 0:
            fppSql = """
            INSERT INTO flight_perd_prnt(
                flight_number, schedule_period_no, selling_class, parent_sell_cls, update_time )
            VALUES(
                '%s', %d, '%s', '%s', NOW() )""" \
            % (flight_number, spn, class_code[i], class_code[i-1])
            printlog(2, "%s" % fppSql)
            cur.execute(fppSql)
            printlog(2, "Inserted %d row(s)" % cur.rowcount)
            i -= 1
        fppSql = """
        INSERT INTO flight_perd_prnt(
            flight_number, schedule_period_no, selling_class, parent_sell_cls, update_time )
        VALUES(
            '%s', %d, '%s', '%s', NOW() )""" \
        % (flight_number, spn, class_code[0], class_code[0])
        printlog(2, "%s" % fppSql)
        cur.execute(fppSql)
        printlog(2, "Inserted %d row(s)" % cur.rowcount)
    cur.close()


def AddScheduleChangeAction(conn, flight_number, spn, city_pair,
                            departure_airport, arrival_airport, class_codes):
    """Add schedule change action."""
    printlog(2, "Add parents for flight %s classes %s (%d)"
             % (flight_number, class_codes, spn))
    cur = conn.cursor()
    for class_code in class_codes:
        lc = len(class_code)
        i = lc - 1
        while i >= 0:
            scaSql = """
            INSERT INTO schd_chng_action(
                flight_number, schedule_period_no, city_pair, selling_class,
                departure_airport, arrival_airport,
                segm_update_flag, seg_cls_updt_flag,
                action_date, action_type, processing_flag, update_time)
            VALUES(
                '%s', %d, %d, '%s',
                '%s', '%s',
                'A', 'A',
                CURRENT_DATE, 'A', 'Y', CURRENT_TIMESTAMP )""" \
            % (flight_number, spn, city_pair, class_code[i],
               departure_airport, arrival_airport)
            printlog(2, "%s" % scaSql)
            cur.execute(scaSql)
            printlog(2, "Inserted %d row(s)" % cur.rowcount)
            i -= 1
    cur.close()


def ProcNew(conn, ssm, userName, groupName):
    """Process new flight."""
    city_pair_id = CheckCityPair(conn,
                                 ssm.departure_airport,
                                 ssm.arrival_airport,
                                 1,
                                 userName,
                                 groupName)
    if city_pair_id == 0:
        print "City pair not OK"
        return -1

    printlog(1, "New flights from %s to %s"
             % (ssm.start_date.strftime("%Y-%m-%d"), ssm.end_date.strftime("%Y-%m-%d")))

    aircraft_config_id = CheckAircraftConfig(conn, ssm.aircraft_code)
    if aircraft_config_id is None:
        print "Aircraft code %s is not configured" % ssm.aircraft_code
        return -1

    print "Aircraft code %s config %s" % (ssm.aircraft_code, aircraft_config_id)

    ssmdates = []
    cdate = ssm.start_date
    while cdate <= ssm.end_date:
        wday = cdate.weekday()+1
        printlog(1, "Date %s (day %d)" % (cdate.strftime("%Y-%m-%d"), wday))
        if wday in ssm.frequency_codes:
            ssmdates.append(cdate)
        cdate += datetime.timedelta(days=1)

    for cdate in ssmdates:
        printlog(1, "Process date %s" % cdate.strftime("%Y-%m-%d"))

    config_no = GetConfigTableNo(conn, ssm.aircraft_code)

    edate = ssm.start_date - datetime.timedelta(days=1)
    spn = IsPeriodToBeExtended(conn,
                               ssm.start_date.strftime("%Y-%m-%d"),
                               ssm.end_date.strftime("%Y-%m-%d"),
                               edate.strftime("%Y-%m-%d"),
                               ssm.frequency_codes,
                               ssm.flight_number,
                               config_no)

    if spn == 0:
        spn = FpFromSsm(conn,
                        ssm.flight_number,
                        ssm.start_date.strftime("%Y-%m-%d"),
                        ssm.end_date.strftime("%Y-%m-%d"),
                        ssm.frequency_code,
                        userName,
                        groupName)

        FpLegsFromSsm(conn,
                      ssm.flight_number,
                      spn,
                      ssm.departure_airport,
                      ssm.departure_terminal,
                      ssm.departure_time,
                      ssm.arrival_airport,
                      ssm.arrival_terminal,
                      ssm.arrival_time,
                      '',
                      ssm.aircraft_code,
                      1)

    for cdate in ssmdates:
        AddFlightSegmDate(conn,
                          ssm.flight_number,
                          cdate,
                          city_pair_id,  # city pair number
                          cdate,
                          ssm.departure_airport,
                          ssm.arrival_airport,
                          ssm.departure_time,
                          ssm.arrival_time,
                          0,          # date change indicator
                          '',         # flight path code
                          ssm.departure_terminal,
                          ssm.arrival_terminal,
                          'A',        # flight schedule status
                          ssm.aircraft_code,
                          'N',        # flight closed flag
                          'N',        # flight boarding flag
                          0,          # number of stops
                          1,          # leg number
                          1,          # segment number
                          spn)
        WriteFlightInfo(conn,
                        ssm.flight_number,
                        cdate,
                        spn,
                        ssm.departure_time,
                        ssm.arrival_time,
                        ssm.departure_airport,
                        ssm.arrival_airport,
                        '',             # Delay Code
                        '',             # Remarks,
                        ssm.aircraft_tail,
                        '',             # Description
                        userName,
                        groupName)
        AddFlightDateLeg(conn,
                         ssm.flight_number,
                         cdate,
                         1,
                         ssm.departure_time,
                         ssm.departure_airport,
                         ssm.arrival_airport,
                         userName,
                         groupName)
        n = 0
        for class_code in ssm.class_codes:
            AddInventorySegment(conn, ssm.flight_number, cdate,
                                int(city_pair_id), class_code[0], ssm.departure_airport, ssm.arrival_airport,
                                1,    # leg number
                                '1',  # segment number
                                '0',  # vob_profile_no
                                0,    # group seat level
                                0,    # seat protect level
                                0,    # limit sale level
                                0,    # overbooking level
                                0,    # posting level
                                0,    # sale notify level
                                0,    # cancel notify level
                                int(ssm.class_seats[n]),  # seat capacity
                                'N',  # segment closed flag
                                'N',  # waiting list closed flag
                                'N',  # waiting list clear inhibit flag
                                'N',  # waiting list release party flag
                                len(ssm.class_codes)-n,  # display_priority
                                spn,  # schedule_period_no,
                                userName, groupName)
            n += 1

    AddFlightPeriodLegs(conn,
                        ssm.flight_number,
                        spn,
                        ssm.departure_airport,
                        ssm.arrival_airport,
                        ssm.departure_time,
                        ssm.arrival_time,
                        0,                 # date change indicator
                        ssm.aircraft_code,  # config table no
                        '',                # flight path code,
                        ssm.departure_terminal,
                        ssm.arrival_terminal,
                        1)                 # leg number

    AddFlightPeriodSegment(conn,
                           ssm.flight_number,
                           spn,
                           city_pair_id,
                           ssm.aircraft_code,
                           'A',
                           1)

    AddFlightPeriod(conn,
                    ssm.flight_number,
                    ssm.departure_airport,
                    ssm.arrival_airport,
                    ssm.start_date.strftime("%Y-%m-%d"),
                    ssm.end_date.strftime("%Y-%m-%d"),
                    ssm.frequency_code,
                    spn,
                    ssm.end_date.strftime("%Y-%m-%d"),
                    userName,
                    groupName)

    AddFlightPeriodClasses(conn,
                           ssm.flight_number,
                           spn,
                           ssm.class_codes)

    AddFlightPeriodSegmentClasses(conn,
                                  ssm.flight_number,
                                  spn,
                                  city_pair_id,
                                  ssm.class_codes,
                                  ssm.class_seats)

    AddFlightPeriodParents(conn,
                           ssm.flight_number,
                           spn,
                           ssm.class_codes)

    AddScheduleChangeAction(conn,
                            ssm.flight_number,
                            spn,
                            city_pair_id,
                            ssm.departure_airport,
                            ssm.arrival_airport,
                            ssm.class_codes)

    return 0
