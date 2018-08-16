"""
Passenger list entries.

@file PaxListEntry.h
"""
import logging

from PnlAdl.PaxData import PaxData

etlp_ticket_number = 0
ADL_LINE_LENGTH = 64

logger = logging.getLogger("web2py.app.bars")


class BookRequestsRec(object):

    action_code = ''
    actn_number = 0
    rqst_code = ''
    request_text = ''
    all_passenger_flag = ''
    all_itinerary_flag = ''

    def __init__(self):
        pass


class PaxListEntry(object):

    book_no = 0
    paxrec = None
    airline_no = 0
    departure_airport = ''
    arrival_airport = ''
    pax_name = ''
    selling_class = ''
    itinerary_reqs = []
    pax_reqs = []
    passenger_no = 0
    pass_code = ''
    no_of_seats = 0
    group_name = ''
    locator = ''
    origin_address = ''
    infant = False
    etickt = False
    etlp_num = ''
    pnlEntry = ''
    SSRs = {}
    pnlSSRs = []
    conn = None
    selling_class_no = -1

    current_line = 0

    def __init__(self,
                 conn,
                 airline_no,
                 a_book_no,
                 a_departure_airport,
                 a_arrival_airport,
                 a_pax_name,
                 a_selling_class,
                 a_itinerary_req,
                 a_pax_req,
                 a_passenger_no,
                 a_pass_code,
                 a_no_of_seats,
                 a_group_name,
                 a_pax_name_rec,
                 a_selling_class_no):
        """Constructor."""
        self.conn = conn
        self.airline_no = airline_no
        self.book_no = a_book_no
        self.departure_airport = str(a_departure_airport).rstrip()
        self.arrival_airport = str(a_arrival_airport).rstrip()
        self.pax_name = str(a_pax_name).rstrip()
        self.selling_class = str(a_selling_class).rstrip()
        self.itinerary_reqs = str(a_itinerary_req).rstrip().split('#')
        self.pax_reqs = str(a_pax_req).rstrip().split('#')
        self.passenger_no = a_passenger_no
        self.pass_code = str(a_pass_code).rstrip()
        self.no_of_seats = a_no_of_seats
        self.group_name = str(a_group_name).rstrip().replace(' ', '')
        self.locator = a_pax_name_rec
        self.infant = False
        self.etickt = False
        self.etlp_num = ''
        self.paxrec = 'FLY'
        self.selling_class_no = a_selling_class_no

    def __lt__(self, other):
        """Used for sorting."""
        if self.selling_class_no > other.selling_class_no:
            return True
        elif self.selling_class_no == other.selling_class_no \
                and self.pax_name < other.pax_name:
            return True
        else:
            return False

    def Clear(self):
        """Reset this thing."""
        self.book_no = 0
        self.departure_airport = ''
        self.arrival_airport = ''
        self.pax_name = ''
        self.selling_class = ''
        self.itinerary_reqs[:] = []
        self.pax_reqs[:] = []
        self.passenger_no = 0
        self.pass_code = ''
        self.no_of_seats = 0
        self.group_name = ''
        self.infant = False
        self.etickt = False
        self.etlp_num = ''
        self.paxrec = 'FLY'
        self.SSRs.clear()
        self.pnlSSRs[:] = []

    def Show(self):
        """Display data."""
        self.GetBookRequests(self.book_no)

        print("Book %d %4s-%-4s: %-55s class %2s(%2d) %-32s %-32s "
              "no %3d %8s %3d %10s %s %s %d"
              % (self.book_no, self.departure_airport, self.arrival_airport,
                 self.pax_name,
                 self.selling_class, self.selling_class_no,
                 self.itinerary_reqs, self.pax_reqs,
                 self.passenger_no, self.pass_code, self.no_of_seats,
                 self.group_name, self.locator,
                 self.origin_address, len(self.SSRs)))

        for ssrk, ssrit in self.SSRs.items():
            print("\t%2d (%c %c) %s %s%d : %s"
                  % (ssrk, ssrit.all_passenger_flag, ssrit.all_itinerary_flag,
                     ssrit.rqst_code, ssrit.action_code, ssrit.actn_number,
                     ssrit.request_text))

    def Append(self, data):
        """Append element to PNL entry."""
        global ADL_LINE_LENGTH
        logger.debug("\tAdd '%s'" % data)
        if (self.current_line + len(data) > ADL_LINE_LENGTH):

            self.pnlEntry += ""
            self.current_line = 0

        self.pnlEntry += data
        self.current_line += len(data)

    def SetEntry(self, aAltFlightNumber, aBoardDate):
        """Set text of PNL file entry."""
        entryBuf = ''
        pd = PaxData()

        pd.paxname = self.pax_name
        pd.locator = self.locator
        pd.grpname = self.group_name

        self.GetBookRequests(self.book_no)

        entryBuf = "1%s" % self.pax_name
        self.pnlEntry = entryBuf
        self.current_line = len(self.pnlEntry)

        if len(self.group_name) > 0:
            entryBuf = "-%s" % self.group_name
            self.Append(entryBuf)

        self.pnlEntry += " "

        infant = etickt = False
        for ssrk, ssrit in self.SSRs.items():
            if (self.SetRequests(ssrk, ssrit)):
                if (ssrit.rqst_code == "INFT"):
                    infant = True
                elif (ssrit.rqst_code == "TKNE"):
                    ssrit.request_text.replace('C', '/')
                    etickt = True
                entryBuf = ".R/%s %s%d %s " \
                           % (ssrit.rqst_code, ssrit.action_code,
                              ssrit.actn_number,
                              ssrit.request_text)
                self.Append(entryBuf)
                pd.AddRemark(str(entryBuf[3:]))

        self.addETLP()
        self.pnlEntry += ""

    def SetLocator(self, locator):
        """Set locator."""
        self.locator = locator

    def GetLocator(self, a_book_no):
        """Get locator for passenger booking number."""
        mid = ''
        book_no = a_book_no
        pnr_book_numb = ''
        book_type = ''
        group_name = ''
        no_of_seats = 0
        book_category = ''
        grup_wait_seats = 0
        grup_rqst_seats = 0
        grup_realtn_pcnt = 0
        origin_branch_code = ''
        book_agency_code = ''
        book_hdq_agency = ''
        origin_city = ''
        origin_nation = ''
        db_origin_address = ''
        record_locator = ''
        received_from = ''
        tour_code = ''
        amount_paid = 0.0
        booking_status = ''
        scrutiny_flag = ''
        divide_from_no = ''
        divide_to_nos = ''
        first_segm_date = 0
        last_segm_date = 0
        reaccom_prty = 0
        dvd_process_flag = ''
        rdu_process_flag = ''
        grp_process_flag = ''
        nrl_process_flag = ''
        crea_user_code = ''
        crea_dest_id = ''
        crea_date_time = ''
        updt_user_code = ''
        updt_dest_id = ''
        updt_date_time = ''
        bn_date1 = ''
        bn_date2 = ''
        rval = 0

        cur = self.conn.cursor()

        logger.info("Get book data for number %d" % a_book_no)

        bn_stmt = """
            SELECT pnr_book_numb,
                    book_type,
                    group_name,
                    no_of_seats,
                    book_category,
                    grup_wait_seats,
                    grup_rqst_seats,
                    grup_realtn_pcnt,
                    origin_branch_code,
                    book_agency_code,
                    book_hdq_agency,
                    origin_city,
                    origin_nation,
                    origin_address,
                    record_locator,
                    received_from,
                    tour_code,
                    amount_paid,
                    booking_status,
                    scrutiny_flag,
                    divide_from_no,
                    divide_to_nos,
                    first_segm_date,
                    last_segm_date,
                    first_segm_date,
                    last_segm_date,
                    reaccom_prty,
                    dvd_process_flag,
                    rdu_process_flag,
                    grp_process_flag,
                    nrl_process_flag,
                    create_user,
                    create_group,
                    create_time,
                    update_user,
                    update_group,
                    update_time
            FROM bookings
            WHERE book_no = %s""" % book_no
        logger.debug(bn_stmt)
        cur.execute(bn_stmt)

        for row in cur:
            pnr_book_numb = row[0]
            book_type = row[1]
            group_name = row[2]
            no_of_seats = row[3]
            book_category = row[4]
            grup_wait_seats = row[5]
            grup_rqst_seats = row[6]
            grup_realtn_pcnt = row[7]
            origin_branch_code = row[8]
            book_agency_code = row[9]
            book_hdq_agency = row[10]
            origin_city = row[11]
            origin_nation = row[12]
            db_origin_address = row[13]
            record_locator = row[14]
            received_from = row[15]
            tour_code = row[16]
            amount_paid = row[17]
            booking_status = row[18]
            scrutiny_flag = row[19]
            divide_from_no = row[20]
            divide_to_nos = row[21]
            first_segm_date = row[22]
            last_segm_date = row[23]
            reaccom_prty = row[24]
            dvd_process_flag = row[25]
            rdu_process_flag = row[26]
            grp_process_flag = row[27]
            nrl_process_flag = row[28]
            crea_user_code = row[29]
            crea_dest_id = row[30]
            crea_date_time = row[31]
            updt_user_code = row[32]
            updt_dest_id = row[33]
            updt_date_time = row[34]

            logger.debug("\t\tpnr_book_numb      : %s \n"
                     "\t\tbook_type          : %s \n"
                     "\t\tgroup_name         : %s \n"
                     "\t\tno_of_seats        : %d \n"
                     "\t\tbook_category      : %s \n"
                     "\t\tgrup_wait_seats    : %d \n"
                     "\t\tgrup_rqst_seats    : %d \n"
                     "\t\tgrup_realtn_pcnt   : %d \n"
                     "\t\torigin_branch_code : %s \n"
                     "\t\tbook_agency_code   : %s \n"
                     "\t\tbook_hdq_agency    : %s \n"
                     "\t\torigin_city        : %s \n"
                     "\t\torigin_nation      : %s \n"
                     "\t\torigin_address     : %s \n"
                     "\t\trecord_locator     : %s \n"
                     "\t\treceived_from      : %s \n"
                     "\t\ttour_code          : %s \n"
                     "\t\tamount_paid        : %.2f \n"
                     "\t\tbooking_status     : %s \n"
                     "\t\tscrutiny_flag       : %s \n"
                     "\t\tdivide_from_no     : %s \n"
                     "\t\tdivide_to_nos      : %s \n"
                     "\t\tfirst_segm_date    : %s \n"
                     "\t\tlast_segm_date     : %s \n"
                     "\t\treaccom_prty       : %d \n"
                     "\t\tdvd_process_flag    : %s \n"
                     "\t\trdu_process_flag    : %s \n"
                     "\t\tgrp_process_flag    : %s \n"
                     "\t\tnrl_process_flag    : %s \n"
                     "\t\tcrea_user_code     : %s \n"
                     "\t\tcrea_dest_id       : %s \n"
                     "\t\tcrea_date_time     : %s \n"
                     "\t\tupdt_user_code     : %s \n"
                     "\t\tupdt_dest_id       : %s \n"
                     "\t\tupdt_date_time     : %s "
                     % (pnr_book_numb,
                        book_type,
                        group_name,
                        no_of_seats,
                        book_category,
                        grup_wait_seats,
                        grup_rqst_seats,
                        grup_realtn_pcnt,
                        origin_branch_code,
                        book_agency_code,
                        book_hdq_agency,
                        origin_city,
                        origin_nation,
                        db_origin_address,
                        record_locator,
                        received_from,
                        tour_code,
                        amount_paid,
                        booking_status,
                        scrutiny_flag,
                        divide_from_no,
                        divide_to_nos,
                        first_segm_date,
                        last_segm_date,
                        reaccom_prty,
                        dvd_process_flag,
                        rdu_process_flag,
                        grp_process_flag,
                        nrl_process_flag,
                        crea_user_code,
                        crea_dest_id,
                        crea_date_time,
                        updt_user_code,
                        updt_dest_id,
                        updt_date_time))
            self.locator = str(pnr_book_numb).rstrip()
            self.origin_address = str(db_origin_address).rstrip()
        cur.close()
        return rval

    def CodeShare(self, aAltFlightNumber, aBoardDate):
        """Add marketing element."""
        logger.info("Check origin_address '%s'" % self.origin_address)
        if (self.origin_address == "MUCQSSA"
                or self.origin_address == "MUCCSSA"):
            codeShareBuf = ".M/%s%c%c%c%s%s " \
                           % (aAltFlightNumber, self.selling_class[0],
                              aBoardDate[0], aBoardDate[1],
                              self.departure_airport, self.arrival_airport)
            self.Append(codeShareBuf)

    def GetBookRequests(self, a_book_no):
        """Get booking requests."""
        book_no = 0
        rqst_seqn_no = 0
        indicator = ''
        rqst_code = ''
        action_code = ''
        actn_number = ''
        request_text = ''
        request_vals = ''
        br_query = ''
        all_passenger_flag = ''
        all_itinerary_flag = ''
        n = 0
        request_nostr = ''

        logger.debug("Get booking requests for book no %d requests '%s'"
                 % (self.book_no, request_nostr))

        n = 0
        book_no = a_book_no

        br_query = """SELECT DISTINCT br.rqst_sequence_no,
            br.indicator, br.rqst_code,
            br.action_code, br.actn_number,
            br.request_text,
            br.all_pax_flag, br.all_itinerary_flag
        FROM book_requests br, service_requests sr
        WHERE br.book_no = %d
        AND br.rqst_code = sr.rqst_code
        AND sr.company_Code = '%s'
        AND br.indicator = sr.indicator
        AND sr.arpt_action_flag = 'Y' """ \
            % (book_no, 'ZZ')

        logger.debug("\t%s" % br_query)
        cur = self.conn.cursor()
        cur.execute(br_query)

        for row in cur:
            book_request = BookRequestsRec()
            rqst_seqn_no = row[0]
            indicator = row[1]
            rqst_code = row[2]
            action_code = row[3]
            actn_number = row[4]
            request_text = row[5]
            all_passenger_flag = row[6]
            all_itinerary_flag = row[7]
            book_request.rqst_code = str(rqst_code).rstrip()
            if (book_request.action_code == "INFT"):
                infant = True
            elif (book_request.action_code == "TKNE"):
                etickt = True
            book_request.action_code = str(action_code).rstrip()
            if actn_number[0].isdigit():
                book_request.actn_number = int(actn_number)
            else:
                book_request.actn_number = 0
            book_request.request_text = str(request_text).rstrip()
            book_request.all_passenger_flag = all_passenger_flag[0]
            book_request.all_itinerary_flag = all_itinerary_flag[0]
            logger.debug("\t\t\t%2d : %s %s%d %s"
                     % (rqst_seqn_no, book_request.rqst_code,
                        book_request.action_code, book_request.actn_number,
                        book_request.request_text))
            self.SSRs[rqst_seqn_no] = book_request
        cur.close()
        return 0

    def SetRequests(self, no, ssr):
        """
        Check remarks.

        @param           no                   request number
        @param           ssr                  special service requests
        @return one when found, zero when not found
        """
        itencpi = 0
        paxcpi = 0
        paxtmpi = 0

        itenflg = ssr.all_itinerary_flag
        paxflg = ssr.all_passenger_flag

        # Break up itinerary into tokens seperated by '#'
        logger.debug("Passenger requests %s itinerary requests %s"
                 % (self.pax_reqs, self.itinerary_reqs))

        if (itenflg == 'N' and paxflg == 'N'):
            # Check itinerary and passenger
            logger.debug("Check itinerary and passenger no[%d] itinerary[%c]"
                          " pax[%c] itenflg[%s] paxflg[%s]"
                          % (no, itenflg, paxflg, self.itinerary_reqs, self.pax_reqs))
            for paxcp in self.pax_reqs:
                if paxcp == '':
                    continue
                paxcpi = int(paxcp)
                logger.debug("Check pax number %d" % paxcpi)
                for itencp in self.itinerary_reqs:
                    itencpi = int(itencp)
                    logger.debug("Check itinerary number %d" % itencpi)
                    if (itencpi == paxcpi):
                        if (paxcpi == no):
                            logger.debug("Found itinerary/pax number %d"
                                     % paxcpi)
                            self.AddSsr(ssr)
                            return 1
        elif (itenflg == 'Y' and paxflg == 'N'):
            # Check itinerary only
            logger.debug("Check itinerary no[%d] itinerary[%s] pax[%s]"
                     " itenflg[%c] paxflg[%c]"
                     % (no, self.itinerary_reqs, self.pax_reqs, itenflg, paxflg))
            for paxcp in self.pax_reqs:
                if paxcp == '':
                    continue
                paxcpi = int(paxcp)
                logger.debug("Check pax number %d" % paxcpi)
                if (paxcpi == no):
                    logger.debug("Found pax number %d" % no)
                    self.AddSsr(ssr)
                    return 1
        elif (itenflg == 'N' and paxflg == 'Y'):
            # Check passenger only
            logger.debug("Check passenger no[%d] itinerary[%s] pax[%s]"
                     " itenflg[%c] paxflg[%c]"
                     % (no, self.itinerary_reqs, self.pax_reqs, itenflg, paxflg))
            for itencp in self.itinerary_reqs:
                if itencp == '':
                    continue
                itencpi = int(itencp)
                logger.debug("Check itinerary number %d" % itencpi)
                if (itencpi == no):
                    logger.debug("Found itinerary number %d" % no)
                    self.AddSsr(ssr)
                    return 1
        else:
            logger.debug("Skip passenger no[%d] itinerary[%s] pax[%s]"
                     " itenflg[%c] paxflg[%c]"
                     % (no, self.itinerary_reqs, self.pax_reqs, itenflg, paxflg))
            return 0
        logger.debug("Could not find itinerary/passenger number %d" % no)
        return 0

    def AddSsr(self, ssr):
        """Add an SSR."""
        if (ssr.rqst_code != "TKNE"):
            self.pnlSSRs.append(ssr)

    def List(self):
        """Display stuff."""
        print("%s\t%s\t%s"
              % (self.locator, self.selling_class, self.pax_name))
        self.ListRequests()
        return 0

    def ListRequests(self):
        """Display SSRs."""
        for bi in self.pnlSSRs:
            print("\t%s %s %d %s"
                  % (bi.rqst_code, bi.action_code, bi.actn_number,
                     bi.request_text))
        return len(self.pnlSSRs)

    def ShowRequests(self):
        """Add SSR."""
        etickt_number = ''
        for bi in self.pnlSSR:
            if (bi.rqst_code == "TKNE"):
                etickt_number = bi.rqst_code
            print(".R/%s %s%d %s "
                  % (bi.rqst_code, bi.action_code, bi.actn_number,
                     bi.request_text))
        return len(self.pnlSSRs), etickt_number

    def GetRequestCount(self):
        """Get number of SSRs."""
        if get_verbose() >= 2:
            for bi in self.pnlSSRs:
                print("%s%d %s %s"
                      % (bi.action_code, bi.actn_number, bi.rqst_code,
                         bi.request_text))
        return len(self.pnlSSRs)

    def addETLP(self):
        '''Add TKNE remark.'''
        etlp_string = ''
        if (self.etickt):
            return

        etlp_string = ".R/TKNE HK1 %03d%07d%03d " \
                      % (self.airline_no, self.book_no, self.passenger_no)
        self.Append(etlp_string)
        if (self.infant):
            etlp_string = " .R/TKNE HK1 INF%03d%07d%03d " \
                          % (self.airline_no, self.book_no, self.passenger_no)
            self.Append(etlp_string)
        return

    def ReadBuf(self, pdata, classnam, arrive):
        """Read buffer thing."""
        if len(pdata) == 0:
            return 0
        logger.info("pax [%s]" % pdata)
        selling_class = classnam
        arrival_airport = arrive
        elements = pdata.split('.')
        self.ReadName(elements[0])
        i = 1
        while i < len(elements):
            self.ReadElement(elements[i])
            i += 1
        return 0

    def ReadName(self, ndata):
        """Read passenger name."""
        nel = ndata.split('-')
        paxcount = ''
        found = nel[0].find_first_not_of("1234567890")
        if found is None:
            print("Invalid name '%s'", nel[0])
            return 1
        paxcount = nel[0][0:found]
        no_of_seats = int(paxcount)
        logger.info("\tcount %d" % no_of_seats)
        pax_name = nel[0][found:].rstrip()
        logger.info("\tname '%s'" % pax_name)
        if (len(nel) > 1 and len(nel[1]) > 0 and nel[1][1] != '/'):
            group_name = nel[1].rstrip()
            logger.info("\tgroup '%s'" % group_name)
        return 0

    def ReadElement(self, edata):
        """Read marketing element."""
        indata = ''
        marketflt = ''
        incomingflt = ''
        outgoingflt = ''
        if (edata[0] == "L"):
            locator = edata[2:].rstrip()
            logger.info("\tlocator '%s'" % locator)
        elif (edata[0] == "R"):
            self.ReadRemarks(edata[2:])
        elif (edata[0] == "M"):
            marketflt = edata[2:].rstrip()
            if (len(marketflt) <= 9):
                print("Marketing element '%s' not valid" % marketflt)
                return 1
            else:
                indata = marketflt.substr(0, marketflt.length()-9)
                logger.info("\tmarketing '%s' for %s" % (marketflt, indata))
        elif (edata[0] == "I"):
            incomingflt = edata[2:].rstrip()
            logger.info("\tincoming flight %s" % incomingflt)
        elif (edata[0] == "O"):
            outgoingflt = edata[2:].rstrip()
            logger.info("\toutgoing flight %s" % outgoingflt)
        else:
            logger.info("\tother '%s'" % edata)
        return 0

    def ReadRemarks(self, rdata):
        """Read SSRs."""
        ssr = BookRequestsRec()
        chekin = ''
        inft = ''
        ssr.rqst_code = rdata[0:4]
        if (ssr.rqst_code == "TKNE"):
            if (len(rdata) < 9):
                print("Invalid e-ticket %s" % rdata)
                return 1
            elif (rdata[9:12] == "INF"):
                infant = True
                logger.info("\tinfant e-ticket '%s'" % rdata)
            elif (rdata[5:8] != "HK1"):
                print("Action code and number is '%s' and not HK1"
                      % rdata.substr(5, 3))
                return 1
            elif (self.etickt):
                print("Duplicate e-ticket '%s'" % rdata)
                return 1
            etickt = True
        elif (ssr.rqst_code == "TKNE"):
            if (len(rdata) < 9):
                print("Invalid ticket %s" % rdata)
                return 1
            elif (rdata[9:12] == "INF"):
                infant = True
                logger.info("\tinfant ticket '%s'" % rdata)
            elif (etickt):
                print("Duplicate ticket")
                return 1
            etlp_num = rdata[9:]
            logger.info("\tticket '%s'" % etlp_num)
            etickt = False
        elif (ssr.rqst_code == "CKIN"):
            chekin = rdata[5:].rstrip()
            logger.info("\tcheckin '%s'" % chekin)
        elif (ssr.rqst_code == "INFT"):
            infant = True
            inft = rdata[5:].rstrip()
            logger.info("\tinfant '%s'" % inft)
        else:
            logger.info("\tremark '%s'" % rdata)
        ssr.action_code = rdata[5:7]
        ssr.actn_number = int(rdata[7])
        ssr.request_text = rdata[9:]
        if (ssr.rqst_code != "TKNE"):
            self.pnlSSRs.append(ssr)

        return 0


def sortPaxList(ple1, ple2):
    """Used to sort passenger list."""
    if (ple1.selling_class < ple2.selling_class):
        return True
    elif (ple1.paxrec < ple2.paxrec):
        return True
    elif (ple1.pax_name < ple2.pax_name):
        return True
    else:
        return False


def ReadAltFlightNumber(conn, aFlightNumber, aBoardDate):
    """Read code share flight number."""
    sqlAltFlightNumberStr = ''
    altFlightNumber = ''
    sqlAltFlightNumberStr = \
        "SELECT dup_flight_number FROM flight_shared_leg" \
        " WHERE flight_date='%s' AND flight_number='%s'" \
        % (aBoardDate, aFlightNumber)
    logger.debug("\t%s" % sqlAltFlightNumberStr)
    cur = conn.cursor()
    cur.execute(sqlAltFlightNumberStr)
    altFlightNumber = None
    for row in cur:
        altFlightNumber = str(row[0]).rstrip()
    return altFlightNumber
