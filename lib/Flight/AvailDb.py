"""
Availability queries.
"""

from Flight.FlightData import FlightData
# import Flight.FlightData
from BarsLog import blogger
from Ssm.SsmDb import GetCityPair


def get_selling_conf(conn, aCompanyCode):
    """Get selling configuration for company."""
    blogger().info("Selling configuration for company %s" % aCompanyCode)
    AvlSql = \
    "SELECT selling_class, cabin_code " \
    "FROM selling_conf " \
    "WHERE company_code = '%s' " \
    "ORDER BY cabin_code " \
        % (aCompanyCode)
    blogger().debug("%s" % AvlSql)
    cur = conn.cursor()
    cur.execute(AvlSql)
    blogger().debug("Selected %d row(s)" % cur.rowcount)
    selling_classs = []
    city_pair_id = 0
    for row in cur:
        blogger().debug("Selling configuration class %s cabin %s" % (row[0], row[1]))
        selling_classs.append(str(row[0]))

    cur.close()
    return selling_classs


def get_avail_flights(conn, fdate1, fdate2, city_pair,
                      departure_airport, arrival_airport,
                      selling_class, company_code):
    blogger().info("Available flights depart %s arrive %s (%d) start %s end %s class %s company %s" %
             (departure_airport, arrival_airport, city_pair,
              fdate1, fdate2,
              selling_class, company_code))
    AvlSql = \
        """
        SELECT DISTINCT fsd.flight_number,   fsd.board_date,
            fsd.departure_time,     fsd.city_pair,
            isg.departure_city,     isg.arrival_city,
            fsd.departure_airport,  fsd.arrival_airport,
            fsd.flight_path_code,   fsd.arrival_time,
            fsd.date_change_ind,    fsd.departure_terminal,
            fsd.arrival_terminal,   fsd.no_of_stops,
            fsd.aircraft_code,      fsd.flight_date,
            sc.cabin_code,          isg.leg_number,
            isg.city_pair,       isg.selling_class,
            isg.limit_sale_level,     isg.seat_capacity,
            isg.overbooking_percnt, isg.nett_sngl_sold,
            isg.nett_group_sold,     isg.nett_nrev_sold,
            isg.segm_sngl_sold,     isg.segm_group_sold,
            isg.segm_nrev_sold,     isg.seat_protect_level,
            isg.display_priority,   fsd.flgt_sched_status,
            isg.segment_closed_flag, fsd.flight_closed_flag,
            fsd.flight_brdng_flag,   isg.ob_profile_no,
            fp.via_cities,          fp.schedule_period_no
        FROM flight_segment_dates fsd, flight_periods fp, inventry_segment isg, selling_conf sc
        WHERE fsd.board_date >= '%s'
        AND fsd.board_date <= '%s'
        AND isg.flight_number = fsd.flight_number
        AND isg.flight_date = fsd.flight_date
        AND fsd.city_pair = '%s'
        AND fsd.departure_airport = '%s'
        AND fsd.arrival_airport = '%s'
        AND isg.selling_class = '%s'
        AND sc.company_code = '%s'
        AND fp.flight_number = fsd.flight_number
        AND fp.schedule_period_no = fsd.schedule_period_no
        AND fsd.flight_number NOT IN
            (
            SELECT flight_number FROM flight_locked AS flck
            WHERE flck.invalid_time IS NULL AND flck.flight_number = fsd.flight_number AND flck.flight_date = fsd.board_date
            )
        AND fsd.flgt_sched_status IN ('A', 'D', 'M', 'U', 'R')
        AND fp.flgt_sched_status IN ('A', 'D', 'M', 'U', 'R')""" \
        % (fdate1, fdate2, city_pair, departure_airport, arrival_airport, selling_class, company_code)
    blogger().debug("%s" % AvlSql)
    cur = conn.cursor()
    cur.execute(AvlSql)

    aircraft_code = ''
    cs = []
    flights = []
    blogger().debug("Selected %d row(s)" % cur.rowcount)
    for row in cur:
        class_code          = row[16]
        flight_number       = row[0]
        departure_date      = row[1]
        departure_time      = row[2]
        arrival_time        = row[9]
        departure_airport   = row[6]
        arrival_airport     = row[7]
        city_pair_number    = int(row[3])
        schedule_period_no  = int(row[37])

        fd = FlightData(class_code,
                        flight_number, departure_date,
                        departure_time, arrival_time,
                        departure_airport, arrival_airport,
                        None, None,
                        city_pair,
                        company_code,
                        aircraft_code,
                        schedule_period_no,
                        cs)
        flights.append(fd)

    cur.close()
    return flights


def ReadAvailDb(conn, company_code, lboard_date, city_pair_no,
                depr_airport, arrv_airport):
    blogger().info("Available flights depart %s arrive %s date %s"
             % (depr_airport, arrv_airport, lboard_date))
    if city_pair_no is None:
        city_pair_no = GetCityPair(conn, departAirport, arriveAirport)
    AvlSql = """
    SELECT fsd.board_date, fsd.flight_number,
        fsd.city_pair, sc.cabin_code,
        isg.leg_number, fsd.flight_date,
        isg.city_pair, isg.departure_city,
        isg.arrival_city,
        fsd.departure_airport, fsd.arrival_airport,
        fsd.flight_path_code, fsd.departure_time,
        fsd.arrival_time, fsd.date_change_ind,
        fsd.departure_terminal, fsd.arrival_terminal,
        fsd.no_of_stops, fsd.aircraft_code,
        isg.selling_class,
        isg.limit_sale_level, isg.seat_capacity,
        isg.overbooking_percnt, isg.nett_sngl_sold,
        isg.nett_group_sold, isg.nett_nrev_sold,
        isg.seat_protect_level, isg.display_priority,
        fsd.flgt_sched_status, isg.segment_closed_flag,
        fsd.flight_closed_flag, fsd.flight_brdng_flag,
        isg.ob_profile_no, fsd.schedule_period_no
        FROM flight_segment_dates fsd, inventry_segment isg, selling_conf sc
        WHERE fsd.board_date = '%s'
        AND isg.flight_number = fsd.flight_number
        AND isg.flight_date = fsd.flight_date
        AND fsd.city_pair = %d
        AND fsd.departure_airport = '%s'
        AND fsd.arrival_airport = '%s'
        AND isg.selling_class = sc.selling_class
        AND sc.company_code = '%s'""" \
    % (lboard_date, city_pair_no, depr_airport, arrv_airport, company_code)
    blogger().debug("%s" % AvlSql)
    cur = conn.cursor()
    cur.execute(AvlSql)

    blogger().debug("Selected %d row(s)" % cur.rowcount)
    flights = []
    for row in cur:
        blogger().info("Flight %s date %s cabin %s depart %s arrive %s class %s schedule %d" \
                 % (row[1], row[0], row[3], str(row[12])[0:5], str(row[13])[0:5], row[19], row[33]))
        class_code          = row[19]
        flight_number       = row[1]
        departure_date      = row[0]
        departure_time      = row[12]
        arrival_time        = row[13]
        departure_airport   = row[9]
        arrival_airport     = row[10]
        departure_terminal = row[15]
        arrival_terminal = row[16]
        aircraft_code = row[18]

        city_pair_number    = int(row[2])
        schedule_period_no  = int(row[33])
        fd = FlightData(class_code,
                        flight_number, departure_date,
                        departure_time, arrival_time,
                        departure_airport, arrival_airport,
                        None, None,
                        city_pair_number,
                        company_code,
                        aircraft_code,
                        schedule_period_no,
                        None)
        flights.append(fd)

    cur.close()
    return flights
