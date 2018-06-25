"""
Passenger name list (PNL) messages.

@file PaxList.py
"""

from BarsLog import printlog, get_verbose
from PnlAdl.PaxListEntry import PaxListEntry, ReadAltFlightNumber

groupCounter = 0

res = ""


def nextGroup():
    """Get the next group identifier for the current PNL/ADL."""
    global res
    global groupCounter
    groupCounter += 1
    n = groupCounter

    if n < 26:
        res = str(chr(ord('A') + n))
    else:
        res = str(chr(ord('A') + (n / 26)))
        res += str(chr(ord('A') + (n % 26)))

    return res


class PaxList(object):
    """Passenger name list (PNL) messages."""
    booking_classes = {}
    DepartAirport = ''
    FlightNumber = ''
    BoardDate = None
    AirlineNo = 0
    conn = None
    pg = {}
    paxListEntries = []
    sellingClasses = ''

    def __init__(self, conn, aAirlineNo, aAltFlightNumber, aBoardDate,
                 aSellingClasses):
        """Initialize variables to be used later."""
        self.conn = conn
        self.AirlineNo = aAirlineNo
        self.AltFlightNumber = aAltFlightNumber
        self.BoardDate = aBoardDate
        self.sellingClasses = aSellingClasses

    def PnlHeader(self):
        """Print PNL file header."""
        print("MUCPPSA")
        print(".JNB7USA 151245")
        print("PNL")
        print("%s/%s %s PART 1" %
              (self.FlightNumber, self.BoardDate.strftime('%d%b%Y').upper(),
               self.DepartAirport))
        print("CFG/002C186Y")
        print("RBD Y/YCEFGJKORZAUSBMPDITHQVWLXN")

    def AdlHeader(self):
        """Print PNL file header."""
        print("MUCPPSA")
        print(".JNB7USA 151245")
        print("ADL")
        print("%s/%s %s PART 1"
              % (self.FlightNumber, self.BoardDate, self.DepartAirport))
        print("CFG/002C186Y")
        print("RBD Y/YCEFGJKORZAUSBMPDITHQVWLXN")

    def PnlFooter(self):
        """Print PNL file footer."""
        print("ENDPNL\n=\n\n\nNNNN")

    def AdlFooter(self):
        """Print ADL file footer."""
        print("ENDADL\n=\n\n\nNNNN")

    def Add(self, ple):
        """Add entry to vector of passengers."""
        self.paxListEntries.append(ple)

    def GetClassCount(self):
        """Get number of passengers for each class."""

        booking_class = '?'

        if (0 == len(self.paxListEntries)):
            return

        for it in self.paxListEntries:
            booking_class = it.selling_class[0]
            mapit = self.booking_classes.get(booking_class)
            if mapit is None:
                self.booking_classes[booking_class] = 1
            else:
                self.booking_classes[booking_class] += 1
            printlog(2, "Booking class %c : %d"
                     % (booking_class, self.booking_classes[booking_class]))

        if get_verbose():
            for k, v in self.booking_classes.items():
                print("Class %c : %d passengers" % (k, v))

    def List(self):
        """Display the whole lot."""
        for it in self.paxListEntries:
            it.List()

    def Show(self):
        """Print out ADL file."""
        booking_class = ''
        class_count = 0

        if len(self.paxListEntries) == 0:
            return

        n = len(self.paxListEntries)
        i = 0
        previt = self.paxListEntries[0]
        i += 1
        while i < len(self.paxListEntries):
            it = self.paxListEntries[i]
            if it.book_no == previt.book_no:
                if len(previt.group_name) == 0:
                    previt.group_name = str(nextGroup())
                printlog(2, "Set group name for %s to %s"
                         % (previt.pax_name, previt.group_name))
                it.locator = str("")
                it.group_name = previt.group_name
                printlog(2, "Set group name for %s to %s and locator to '%s'"
                         % (it.pax_name, it.group_name, it.locator))
            previt.SetEntry(self.AltFlightNumber, self.BoardDate)
            previt = it
            i += 1
        previt.SetEntry(self.AltFlightNumber, self.BoardDate)

        self.GetClassCount()
        self.paxListEntries.sort()

        # self.paxListEntries[0].SetLocator()

        i = 0
        it = self.paxListEntries[0]
        booking_class = it.selling_class[0]
        class_count = self.booking_classes.get(booking_class)
        if class_count is None:
            class_count = 0
        print("-%3s%03d%c" % (it.arrival_airport, class_count, booking_class))
        previt = it
        i += 1
        while i < n:
            it = self.paxListEntries[i]
            print("%s" % previt.pnlEntry, end='')
            if previt.book_no != it.book_no:
                print(" .L/%s" % previt.locator)
            else:
                print("")
            if previt.selling_class != it.selling_class:
                booking_class = it.selling_class[0]
                class_count = self.booking_classes.get(booking_class)
                if class_count is None:
                    class_count = 0
                print("-%3s%03d%c" % (it.arrival_airport, class_count,
                      booking_class))
            previt = it
            i += 1
        print("%s" % previt.pnlEntry)

    def ReadDb(self, aFlightNumber, aBoardDate, aDepartAirport):
        """
        Read and process booked passengers for flight.

        SELECT it.book_no, it.departure_airport, it.arrival_airport,
                it.departure_time depart,
                it.arrival_time arrive,
                pa.pax_name, it.selling_class,
                it.request_nos itinerary_req, pa.request_nos pax_req,
                pa.pax_code, pa.pax_no, bo.no_of_seats, group_name
        FROM (
            SELECT distinct fsd2.*
            FROM flight_segment_dates AS fsd
            INNER JOIN flight_segment_dates AS fsd2
                ON fsd2.flight_number = fsd.flight_number
                AND fsd2.flight_date = fsd.flight_date
                AND fsd2.leg_number <= fsd.leg_number
                AND fsd2.arrival_airport <> fsd.departure_airport
            WHERE fsd.flight_number= '%s' AND fsd.board_date = '%s' )
        AS fsd3 INNER JOIN itineraries AS it
            ON it.flight_number = fsd3.flight_number
            AND it.flight_date = fsd3.board_date
            AND it.departure_airport = fsd3.departure_airport
            AND it.arrival_airport = fsd3.arrival_airport
        INNER JOIN bookings AS bo ON bo.book_no = it.book_no
        INNER JOIN passenger AS pa ON pa.book_no = it.book_no
        INNER JOIN action_codes AS ac
            ON it.reserve_status = ac.action_code
            AND ac.pnl_adl_flag = 'Y'
        WHERE it.itinerary_type <> 'I'
        AND pa.pax_no > 0
        AND pa.pax_code <> 'INF'
        AND it.status_flag <> 'X'
        AND bo.status_flag <> 'X'
        ORDER BY it.book_no, pa.pax_name
        """
        # cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur1 = self.conn.cursor()
        cur2 = self.conn.cursor()
        self.FlightNumber = aFlightNumber
        self.DepartAirport = aDepartAirport
        self.AltFlightNumber = ReadAltFlightNumber(self.conn,
                                                   self.FlightNumber,
                                                   self.BoardDate)
        printlog(1, "Get pax data for flight '%s' date '%s'"
                 % (self.FlightNumber, self.BoardDate))
        sqlStr1 = """SELECT it.book_no, it.departure_airport, it.arrival_airport,
                it.departure_time depart,
                it.arrival_time arrive,
                it.selling_class,
                it.request_nos itinerary_req,
                bo.pax_name_rec, bo.no_of_seats, bo.group_name
                FROM itineraries AS it, bookings AS bo
                WHERE it.flight_number = '%s'
                AND it.flight_date = '%s'
                AND it.book_no = bo.book_no
                """ \
                % (aFlightNumber, aBoardDate)

        """
                    SELECT distinct fsd2.*
                    FROM flight_segment_dates AS fsd
                    INNER JOIN flight_segment_dates AS fsd2
                        ON fsd2.flight_number = fsd.flight_number
                        AND fsd2.flight_date = fsd.flight_date
                        AND fsd2.leg_number <= fsd.leg_number
                        AND fsd2.arrival_airport <> fsd.departure_airport
                    WHERE fsd.flight_number= '%s' AND fsd.board_date = '%s' )
                AS fsd3 INNER JOIN itineraries AS it
                    ON it.flight_number = fsd3.flight_number
                    AND it.flight_date = fsd3.board_date
                    AND it.departure_airport = fsd3.departure_airport
                    AND it.arrival_airport = fsd3.arrival_airport
                INNER JOIN bookings AS bo ON bo.book_no = it.book_no
                INNER JOIN passenger AS pa ON pa.book_no = it.book_no
                INNER JOIN action_codes AS ac
                    ON it.reserve_status = ac.action_code
                    AND ac.pnl_adl_flag = 'Y'
                WHERE it.itinerary_type <> 'I'
                AND pa.pax_no > 0
                AND pa.pax_code <> 'INF'
                AND it.status_flag <> 'X'
                AND bo.status_flag <> 'X'
                ORDER BY it.book_no, pa.pax_name
        """
        printlog(2, "\t%s" % sqlStr1)

        iNoOfRecords = 0
        cur1.execute(sqlStr1)
        for row1 in cur1:
            book_no = row1[0]
            departure_airport = row1[1]
            arrival_airport = row1[2]
            depart = row1[3]
            arrive = row1[4]
            selling_class = row1[5][0]
            selling_class_no = self.sellingClasses.find(selling_class)
            itinerary_req = row1[6]
            pax_name_rec = row1[7]
            no_of_seats = row1[8]
            group_name = row1[9]
            if self.DepartAirport == '':
                self.DepartAirport = str(departure_airport).rstrip()
            sqlStr2 = """
                SELECT pa.pax_name, pa.request_nos pax_req, pa.pax_code,
                    pa.pax_no
                FROM passenger AS pa
                WHERE pa.book_no = %d""" % book_no
            printlog(2, "\t%s" % sqlStr2)
            cur2.execute(sqlStr2)
            for row2 in cur2:
                pax_name = row2[0]
                pax_req = row2[1]
                pax_code = row2[2]
                pax_no = row2[3]
                paxListEntry = PaxListEntry(self.conn, self.AirlineNo, book_no,
                                            departure_airport, arrival_airport,
                                            pax_name, selling_class,
                                            itinerary_req, pax_req,
                                            pax_no, pax_code,
                                            no_of_seats, group_name,
                                            pax_name_rec, selling_class_no)
                # paxListEntry.GetLocator(book_no)
                paxListEntry.GetBookRequests(book_no)
                if get_verbose() >= 1:
                    paxListEntry.Show()
                self.Add(paxListEntry)
                iNoOfRecords += 1

        cur2.close()
        cur1.close()
        return 0

    def ReadFile(self, aFlightNumber, aBoardDate, aDepartAirport):
        """Read PNL message."""
        self.FlightNumber = aFlightNumber
        self.DepartAirport = aDepartAirport
        self.AltFlightNumber = ReadAltFlightNumber(self.conn,
                                                   self.FlightNumber,
                                                   aBoardDate)
        # Read existing PNL from database
        pnlBuf = self.ReadPnl(self.FlightNumber, self.BoardDate)
        printlog(1, "%s" % pnlBuf)
        return self.ReadBuf(pnlBuf, True)

    def ReadBuf(self, inBuf, doPnl):
        """Read the buffer thing."""
        n = 0
        classcnt = 0
        classnam = '?'
        classtot = ''
        nclass = 0
        paxdata = ''
        arrive = ''
        fdata = ''
        pd = PaxListEntry()
        pd.Clear()

        # Remove backslashes
        inBuf.replace('\\', '')

        segments = inBuf.split('\n')
        for it in segments:
            n += 1
            printlog(2, "\t\t%d: %s" % n, it.c_str())

        n = len(segments)
        if n < 13:
            print("Too few lines in file (%d)" % n)
            return 1
        printlog(2, "\tread %d lines [%s]" % n, segments[n-2])

        if self.CheckHeader(segments, doPnl):
            return 1

        if segments[n-2][0:4] == "NNNN":
            n -= 1
            printlog(2, "\tRead %d lines : %s" % n, segments[n-1])
        else:
            printlog(1, "Read %d lines [%s]" % n, segments[n-2])

        if doPnl and segments[n-5][0:6] != "ENDPNL":
            print("No ENDPNL (%s)" % segments[n-5])
            return 1

        if (not doPnl) and (segments[n-5][0:6] != "ENDADL"):
            print("No ENDADL (%s)" % segments[n-5])
            return 1

        if segments[n-1][0:4] == "NNNN" or segments[n-2] != "" \
                or segments[n-3] != "" or segments[n-4] != "=":
            print("Invalid trailer")
            return 1

        self.paxListEntries[:] = []
        i = 6
        while i < n - 5:
            fdata = segments[i]
            if fdata[0] >= '0' and fdata[0] <= '9':
                if len(paxdata) > 0:
                    pd.ReadBuf(paxdata, classnam, arrive)
                self.AddGroup(pd)
                self.Add(pd)
                pd.Clear()
                paxdata = segments[i]
                ++classcnt
            elif fdata[0] == '.':
                paxdata += " "
                paxdata += segments[i]
            elif fdata[0] == ' ':
                    paxdata += segments[i]
            elif fdata[0] == '-':
                if len(paxdata) > 0:
                    pd.ReadBuf(paxdata, classnam, arrive)
                self.AddGroup(pd)
                self.Add(pd)
                pd.Clear()
                paxdata.clear()
                if doPnl and classcnt != nclass:
                    print("Class %c has %d of %d pax"
                          % (classnam, classcnt, nclass))
                classcnt = 0
                classnam = fdata[7]
                arrive = segments[i][1:3]
                classtot, = fdata[4:7]
                classtot[4] = 0
                nclass = int(classtot)
                printlog(1, "Class %c %d [%s]" % classnam, nclass, fdata)
            elif (not doPnl) and (fdata[0:3] == "ADD"):
                print("Added pax [%s]" % fdata)
            elif (not doPnl) and (fdata == "DEL"):
                print("Deleted pax [%s]" % fdata)
            else:
                print("Other [%s]" % fdata)
            i += 1
        if len(paxdata) > 0:
            pd.ReadBuf(paxdata, classnam, arrive)
            self.AddGroup(pd)
            self.Add(pd)
            pd.Clear()

        if doPnl and classcnt != nclass:
            print("Class %c has %d of %d pax" % classnam, classcnt, nclass)

        return 0

    def CheckHeader(self, segments, doPnl):
        """Sanity check on message header."""
        if (doPnl and segments[2] != "PNL"):
            print("Not a PNL (%s)" % segments[2])
            return 1

        if (not doPnl) and (segments[2:5] != "ADL"):
            print("Not an ADL (%s)" % segments[2])
            return 1

        flightel = segments[3].split(' ')

        spos = flightel[0].find_first_of("/")
        if spos is None:
            print("Invalid flight element '%s'" % segments[3])
            return 1
        flightNumber = flightel[0][0:spos]
        boardDate = flightel[0][spos+1:]
        departAirport = flightel[1]

        if self.FlightNumber != flightNumber:
            print("Flight number %s should be %s"
                  % flightNumber, self.FlightNumber)
            return 1

        if boardDate != self.BoardDate:
            print("Board date %s should be %s" % (boardDate, self.BoardDate))
            return 1

        if departAirport != self.DepartAirport:
            print("Departure airport %s should be %s"
                  % departAirport, self.DepartAirport)
            return 1

        if segments[4] != "CFG/002C186Y":
            print("Non-standard configuration (%s)" % segments[4])

        return 0

    def AddGroup(self, pd):
        """Add pax group."""
        if len(pd.group_name) == 0:
            printlog(1, "\tno group")
            return

        if len(pd.locator) == 0:
            it = self.pg.find(pd.group_name)
            if it is None:
                printlog(1, "\tno locator for group '%s'" % pd.group_name)
                return
            else:
                pd.locator = it.second
                printlog(1, "\tlocator for group '%s' specified above as '%s'"
                         % (pd.group_name, it.second))
                return

        it = self.pg.find(pd.group_name)
        if it is not None:
            self.pg[pd.group_name] = pd.locator
            printlog(1, "\tlocator for group '%s' set to '%s'"
                     % (pd.group_name, pd.locator))
            return
        printlog(1, "\tlocator for group '%s' specified above as '%s'"
                 % (pd.group_name, it.second))
