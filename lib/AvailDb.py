from FlightData import FlightData
from BarsLog import printlog

def get_selling_conf(conn, aCompanyCode):
    AvlSql = \
    "SELECT selling_cls_code, cabin_code " \
    "FROM selling_conf " \
    "WHERE company_code = '%s' " \
    "ORDER BY cabin_code " \
        % (aCompanyCode)
    printlog(2, "%s" % AvlSql)
    cur = conn.cursor()
    cur.execute(AvlSql)
    printlog(2, "Selected %d row(s)" % cur.rowcount)
    selling_cls_codes = []
    city_pair_id = 0
    for row in cur:
        printlog(1, "Selling configuration class %s cabin %s" % (row[0], row[1]))
        selling_cls_codes.append(str(row[0]))

    cur.close()
    return selling_cls_codes


def get_avail_flights(conn, fdate1, fdate2, city_pair_no,
                      depr_airport, arrv_airport,
                      selling_cls_code, company_code):
    printlog(2, "Available flights depart %s arrive %s (%d) start %s end %s class %s company %s" %
             (depr_airport, arrv_airport, city_pair_no,
              fdate1, fdate2,
              selling_cls_code, company_code))
    AvlSql = \
        """
        SELECT fsd.flight_number,   fsd.board_date,
            fsd.departure_time,     fsd.city_pair_no,
            isg.departure_city,     isg.arrival_city,
            fsd.depr_airport,       fsd.arrv_airport,
            fsd.flight_path_code,   fsd.arrival_time,
            fsd.date_change_ind,    fsd.depr_terminal_no,
            fsd.arrv_terminal_no,   fsd.no_of_stops,
            fsd.aircraft_code,      fsd.flight_date,
            sc.cabin_code,          isg.leg_number,
            isg.city_pair_no,       isg.selling_cls_code,
            isg.limit_sale_lvl,     isg.seat_capacity,
            isg.overbooking_percnt, isg.nett_sngl_sold,
            isg.nett_grup_sold,     isg.nett_nrev_sold,
            isg.segm_sngl_sold,     isg.segm_grup_sold,
            isg.segm_nrev_sold,     isg.seat_protect_lvl,
            isg.display_priority,   fsd.flgt_sched_status,
            isg.segment_closed_flg, fsd.flight_closed_flg,
            fsd.flight_brdng_flg,   isg.ob_profile_no,
            fp.via_cities,          fp.schd_perd_no
        FROM flight_segm_date fsd, flight_periods fp, inventry_segment isg, selling_conf sc
        WHERE fsd.board_date >= '%s'
        AND fsd.board_date <= '%s'
        AND isg.flight_number = fsd.flight_number
        AND isg.flight_date = fsd.flight_date
        AND fsd.city_pair_no = '%s'
        AND fsd.depr_airport = '%s'
        AND fsd.arrv_airport = '%s'
        AND isg.selling_cls_code = '%s'
        AND sc.company_code = '%s'
        AND fp.flight_number = fsd.flight_number
        AND fp.schd_perd_no = fsd.schd_perd_no
        AND fsd.flight_number NOT IN
            (
            SELECT flight_number FROM flight_locked AS flck
            WHERE flck.invalidated_date_time IS NULL AND flck.flight_number = fsd.flight_number AND flck.flight_date = fsd.board_date
            )
        AND fsd.flgt_sched_status IN ('A', 'D', 'M', 'U', 'R')
        AND fp.flgt_sched_status IN ('A', 'D', 'M', 'U', 'R')""" \
        % (fdate1, fdate2, city_pair_no, depr_airport, arrv_airport, selling_cls_code, company_code)
    printlog(2, "%s" % AvlSql)
    cur = conn.cursor()
    cur.execute(AvlSql)

    aircraft_code = ''
    cs = []
    flights = []
    printlog(2, "Selected %d row(s)" % cur.rowcount)
    for row in cur:
        class_code          = row[16]
        flight_number       = row[0]
        departure_date      = row[1]
        departure_time      = row[2]
        arrival_time        = row[9]
        departure_airport   = row[4]
        arrival_airport     = row[5]
        city_pair_number    = int(row[3])
        schedule_period_no  = int(row[37])

        fd = FlightData(class_code,
                        flight_number, departure_date,
                        departure_time, arrival_time,
                        departure_airport, arrival_airport,
                        None, None,
                        city_pair_no,
                        company_code,
                        aircraft_code,
                        schedule_period_no,
                        cs)
        flights.append(fd)

    cur.close()
    return flights
