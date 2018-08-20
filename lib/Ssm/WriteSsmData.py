"""
Write SSM message
@file WriteSsmData.py
"""
import os
import sys
import time
import logging

from ReadDateTime import ReadDate, ReadTime

logger = logging.getLogger("web2py.app.bars")


def GetWeekDay(idate):
    """Get day of week
    @param idate     input date
    @return day number
    """
    # e.g.   12/13/2014
    if not(idate[2] == '/' and idate[5] == '/' and len(idate) == 10):
        print("Invalid date %s\n" % idate)
        return -1

    board_dts = time.strptime(idate, "%m/%d/%y")

    board_weekday = int(board_dts.strftime("%w"))
    return board_weekday


def IntToRoman(ival):
    """
    Convert number to Roman numerals
    @param ival  input value
    @return Roman numerals
    """
    Mm = ["", "M", "MM", "MMM"]
    Cc = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    Xx = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    Ii = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    rstr = Mm[ival/1000]
    rstr += Cc[(ival % 1000)/100]
    rstr += Xx[(ival % 100)/10]
    rstr += Ii[(ival % 10)]

    return rstr


class WriteSsmDataError(Exception):

    def __init___(self, msg, original_exception):
        super(WriteSsmDataError, self).__init__(msg +
                                                (": %s" % original_exception))
        self.original_exception = original_exception
        print("Goodbye cruel world.")
        sys.exit(1)


class WriteSsmData():

    ftype = None               # file type i.e. NEW, CNL, TIM or EQT
    Address = None             # origin address
    Sender = None              # sender address
    TimeMode = None            # time mode - local or UTC
    FlightNumber = None        # flight number
    FlightDateStart = None     # start date
    FlightDateEnd = None       # end date
    DepartCity = None          # departure airport
    DepartTime = None          # departure time
    ArriveCity = None          # arrival airport
    ArriveTime = None          # arrival time
    AircraftCode = None        # aircraft configuration code
    FrequencyCode = None       # frequency code
    Codeshare = None           # codeshare flight number
    SeatCount = None           # number of seats
    BookingClasses = None      # booking classes
    TailNumber = None          # aircraft tail number

    def __init___(self,
                  aftype,
                  aAddress,
                  aSender,
                  aTimeMode,
                  aFlightNumber,
                  aFlightDateStart,
                  aFlightDateEnd,
                  aDepartCity,
                  aDepartTime,
                  aArriveCity,
                  aArriveTime,
                  aAircraftCode,
                  aFrequencyCode,
                  aCodeshare,
                  aTailNumber):
        """ Constructor. """
        self.ftype = aftype
        self.Address = aAddress
        self.Sender = aSender
        self.TimeMode = aTimeMode
        self.FlightNumber = str(aFlightNumber)
        self.FlightDateStart = ReadDate(aFlightDateStart)
        self.FlightDateEnd = ReadDate(aFlightDateEnd)
        self.DepartCity = str(aDepartCity)
        logger.debug("Depart %s" % self.DepartCity)

        self.DepartTime = ReadTime(aDepartTime)
        logger.debug("Depart time '%s'" % self.DepartTime)

        self.ArriveCity = str(aArriveCity)
        logger.debug("Arrive %s" % self.ArriveCity)

        self.ArriveTime = ReadTime(aArriveTime)
        logger.debug("Arrive time '%s'" % self.ArriveTime)

        self.AircraftCode = aAircraftCode
        logger.debug("Aircraft code '%s'" % self.AircraftCode)

        self.FrequencyCode = str(aFrequencyCode)
        logger.debug("Frequency '%s'" % self.FrequencyCode)

        self.Codeshare = aCodeshare
        logger.debug("Codeshare '%s'" % self.Codeshare)

        if self.AircraftCode == "733":
            self.SeatCount = "Y144"
            self.BookingClasses = "YZAUSBMPDITHQVWLXRNGEFKJO144"
        elif self.AircraftCode == "738":
            self.SeatCount = "C2Y186"
            self.BookingClasses = "C002YZAUSBMPDITHQVWLXRNGEFKJO186"
        elif self.AircraftCode == "320":
            self.SeatCount = "Y180"
            self.BookingClasses = "YZAUSBMPDITHQVWLXRNGEFKJO177"
        elif self.ftype == "CNL":
            # No aircraft code needed here
            self.SeatCount = None
            self.BookingClasses = None
        else:
            logger.error("Unknown aircraft code '%s'" % self.AircraftCode)
            raise 1

        if aTailNumber is None and self.ftype != "CNL":
            self.TailNumber = "ZS"
            self.TailNumber += self.DepartCity[0]
            self.TailNumber += self.ArriveCity[0]
            self.TailNumber += (aDepartTime/100)+65
        else:
            TailNumber = aTailNumber

        try:
            # Weekday as a decimal number 0(Sunday), 1(Monday) to 6(Saturday)
            sdate = str(self.FlightDateStart.strftime("%w"))
            if sdate == "0":
                sdate = "7"
            edate = str(self.FlightDateEnd.strftime("%w"))
            if edate == "0":
                edate = "7"

            if sdate not in self.FrequencyCode:
                logger.error("Start %s day of week %d not in frequency %s"
                             % (self.FlightDateStart, sdate,
                                self.FrequencyCode))
                raise WriteSsmDataError

            if edate not in self.FrequencyCode:
                logger.error("End %s day of week %d not in frequency %s"
                             % (self.FlightDateEnd, edate, self.FrequencyCode))
                raise WriteSsmDataError

        except Exception:
            logger.error("Some sort of date error")
            raise WriteSsmDataError

        # logger.debug("Start %s end %s" % date1, date2)

        now = time(0)   # get time now
        if self.TimeMode == "LT":
            nowstruct = time.time()
        elif self.TimeMode == "UTC":
            nowstruct = time.gmtime()
        else:
            logger.error("Invalid time mode %s" % self.TimeMode)
            raise WriteSsmDataError
        self.timenow = nowstruct.strftime("%H%M%S")
        logger.debug("Time is %s" % self.timenow)

    def WriteCnl(self):
        '''Write cancel SSM.'''
        self.obuff = self.Address + "\n" \
            + "." + self.Sender + " " + self.timenow + "\n" \
            + "SSM\n" \
            + self.TimeMode + "\n" \
            + "CNL\n" \
            + self.FlightNumber + "\n" \
            + self.date1 + " " + self.date2 + " " + self.FrequencyCode + "\n"
        # @todo is this legit?
        if len(self.Codeshare) > 0:
            self.obuff = self.obuff + self.DepartCity + self.ArriveCity \
                    + " 10/" + self.Codeshare + "\n"

    def WriteEqt(self):
        '''Write equipment SSM.'''
        self.obuff = self.Address + "\n" \
            + "." + self.Sender + " " + self.timenow + "\n" \
            + "SSM\n" \
            + self.TimeMode + "\n" \
            + "EQT\n" \
            + self.FlightNumber + "\n" \
            + self.date1 + " " + self.date2 + " " + self.FrequencyCode + "\n" \
            + "J " + self.AircraftCode + " XX." + self.SeatCount + " " \
            + self.TailNumber + "\n" \
            + "QQQQQQ 106/" + self.BookingClasses + "\n"

    def WriteNew(self):
        '''Write new flight SSM.'''
        self.obuff = self.Address + "\n" \
            + "." + self.Sender + " " + self.timenow + "\n" \
            + "SSM\n" \
            + self.TimeMode + "\n" \
            + "NEW\n" \
            + self.FlightNumber + "\n" \
            + self.date1 + " " + self.date2 + " " + self.FrequencyCode + "\n" \
            + "J " + self.AircraftCode \
            + " XX." + self.SeatCount + " " + self.TailNumber + "\n" \
            + self.DepartCity + self.DepartTime + " " \
            + self.ArriveCity + self.ArriveTime \
            + " 7\n" \
            + self.DepartCity + self.ArriveCity + " 8/A\n" \
            + self.DepartCity + self.ArriveCity + " 99/0\n"
        if len(self.Codeshare) > 0:
            self.obuff = self.obuff + self.DepartCity + self.ArriveCity \
                + " 10/" + self.Codeshare + "\n"
        if self.AircraftCode == "738":
            self.obuff = self.obuff + self.DepartCity + self.ArriveCity \
                + " 106/C002YZAUSBMPDITHQVWLXRNGEFKJO186\n"
        elif self.AircraftCode == "733":
            self.obuff = self.obuff + self.DepartCity + self.ArriveCity \
                + " 106/YZAUSBMPDITHQVWLXRNGEFKJO144"
        elif self.AircraftCode == "320":
            self.obuff = self.obuff + self.DepartCity + self.ArriveCity \
                + " 106/YZAUSBMPDITHQVWLXRNGEFKJO177"
        else:
            # @todo something
            pass

    def WriteRpl(self):
        '''Write replace flight SSM.'''
        self.obuff = self.Address + "\n" \
            + "." + self.Sender + " " + self.timenow + "\n" \
            + "SSM\n" \
            + self.TimeMode + "\n" \
            + "RPL\n" \
            + self.FlightNumber + "\n" \
            + self.date1 + " " + self.date2 + " " + self.FrequencyCode + "\n" \
            + "J " + self.AircraftCode \
            + " XX." + self.SeatCount + " " + self.TailNumber + "\n" \
            + self.DepartCity + self.DepartTime \
            + " " + self.ArriveCity + self.ArriveTime + " 7\n" \
            + self.DepartCity + self.ArriveCity \
            + " 106/" + self.BookingClasses + "\n"
        if len(self.Codeshare):
            self.obuff = self.obuff + self.DepartCity + self.ArriveCity \
                + " 10/" + self.Codeshare + "\n"

    def WriteTim(self):
        '''Write time change SSM.'''
        obuff = self.Address + "\n" \
            + "." + self.Sender + " " + self.timenow + "\n" \
            + "SSM\n" \
            + self.TimeMode + "\n" \
            + "TIM\n" \
            + self.FlightNumber + "\n" \
            + self.date1 + " " + self.date2 + " " + self.FrequencyCode + "\n" \
            + self.DepartCity + self.DepartTime \
            + " " + self.ArriveCity + self.ArriveTime + "\n"

    def FileName(self):
        '''Generate output file name.'''
        fname = IntToRoman(self.FlightNumber[2:]) + self.FlightDateStart \
            + self.ftype \
            + self.FlightDateEnd

        return fname

    def WriteSsmFile(self, ofname):
        '''Write SSM file.'''
        rv = 0

        if self.ftype == "CNL":
            self.WriteCnl()
        elif self.ftype == "EQT":
            self.WriteEqt()
        elif self.ftype == "NEW":
            self.WriteNew()
        elif self.ftype == "RPL":
            self.WriteRpl()
        elif self.ftype == "TIM":
            self.WriteTim()
        else:
            print("Unknown file type '%s'" % self.ftype)
            raise WriteSsmDataError

        self.obuff += "\n"

        if len(ofname) == 0:
            ofname = "-"

        if ofname != "-":
            logger.debug("Write output file %s" % ofname)
            try:
                pfile = os.popen(ofname, "w")
                pfile.write(self.obuff)
                pfile.close()
            except KeyboardInterrupt:
                try:
                    pfile.close()
                except IOError:
                    pass
                return -1
            except IOError:
                pass
            # obuff += "\03\03\n"
            # fprintf(ofile, "%s", obuff)
        else:
            print("%s" % self.obuff)

        return rv
