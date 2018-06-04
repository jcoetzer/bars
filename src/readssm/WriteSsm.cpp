/**
 * @file WriteSsm.cpp
 *
 * Write SSM message
 */
#define _XOPEN_SOURCE 700

#include <string>
#include <sstream>
#include <iostream>
#include <iomanip>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <time.h>

#include "WriteSsm.h"
#include "SsmDate.hpp"
// #include "DbDate.h"

extern int verbose;

/**
 * Get day of week
 *
 * @param idate     input date
 *
 * @return day number
 */
int GetWeekDay(const char * idate)
{
    struct tm tm;

    //    12/13/2014
    if (!( idate[2] == '/' && idate[5] == '/' && strlen(idate)==10 ))
    {
        fprintf(stderr, "Invalid date %s\n", idate);
        return -1;
    }
    strptime(idate, "%m/%d/%y", &tm);
    return tm.tm_wday;
} // GetWeekDay()


/**
 * Convert number to Roman numerals
 *
 * @param ival  input value
 *
 * @return Roman numerals
 */
std::string IntToRoman(int ival)
{
    std::string rstr;
    std::string M[] = {"","M","MM","MMM"};
    std::string C[] = {"","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"};
    std::string X[] = {"","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"};
    std::string I[] = {"","I","II","III","IV","V","VI","VII","VIII","IX"};

    rstr = M[ival/1000]+C[(ival%1000)/100]+X[(ival%100)/10]+I[(ival%10)];

    return rstr;
} // IntToRoman()

/**
 * Convert date
 *
 * @param datev             input value
 * @param[out] odate_mdy    buffer for date in MDY format, e.g. 04/24/2018
 * @param mdy_len           buffer length
 * @param[out] odate_iata   buffer for date in airline format, e.g. 24APR2018
 * @param[out] iata_len     buffer length
 *
 * @return zero upon success otherwise non-zero
 */
int MakeFlightDate(std::string datev,
                   char * odate_mdy,
                   size_t mdy_len,
                   char * odate_iata,
                   size_t iata_len)
{
    time_t now;
    struct tm dts;
    char arg[64];

    if ( datev.empty() )
    {
        fprintf(stderr, "Empty date\n");
        throw 1;
    }

    strcpy(arg, datev.c_str());

    if ( 0 == strcasecmp(arg, "yesterday") )
    {
        now = time(NULL);
    }
    else if ( 0 == strcasecmp(arg, "today") )
    {
        now = time(NULL);
    }
    else if ( 0 == strcasecmp(arg, "tomorrow") )
    {
        now = time(NULL);
    }
    else
    {
        memset(&dts, 0, sizeof(struct tm));
        // 20JUL
        if ( strlen(arg) == 5 )
        {
            strptime(arg, "%d%b", &dts);
        }
        // 20JUL17
        else if ( strlen(arg) == 7 )
        {
            strptime(arg, "%d%b%y", &dts);
        }
        else if ( strlen(arg) == 10 )
        {
            // 07/20/2017
            if ( arg[2] == '/' && arg[5] == '/' )
            {
                strptime(arg, "%m/%d/%Y", &dts);
            }
            // 2017-07-20
            else if ( arg[4] == '-' && arg[7] == '-' )
            {
                strptime(arg, "%Y-%m-%d", &dts);
            }
            else
            {
                fprintf(stderr, "Invalid 10 character date '%s'\n", arg);
                throw 2;
            }
        }
        else if ( strlen(arg) == 8 )
        {
            // 07/20/17
            if ( arg[2] == '/' && arg[5] == '/' )
            {
                strptime(arg, "%m/%d/%y", &dts);
            }
            else if ( arg[1] == '/' && arg[3] == '/' )
            {
                strptime(arg, "%m/%d/%Y", &dts);
            }
            // 17-07-20
            else if ( arg[2] == '-' && arg[5] == '-' )
            {
                strptime(arg, "%y-%m-%d", &dts);
            }
            else
            {
                fprintf(stderr, "Invalid 8 character date '%s'\n", arg);
                throw 2;
            }
        }
        else if ( strlen(arg) == 9 )
        {
            if ( arg[2] == '/' && arg[4] == '/' )
            {
                strptime(arg, "%m/%d/%Y", &dts);
            }
            else if ( arg[1] == '/' && arg[4] == '/' )
            {
                strptime(arg, "%m/%d/%Y", &dts);
            }
            else
            {
                strptime(arg, "%d%b%Y", &dts);
            }
        }
        // 20JUL17
        else if ( strlen(arg) == 7 )
        {
            strptime(arg, "%d%b%y", &dts);
        }
        // 2017-09-14 10:29
        else if ( strlen(arg) == 16 )
        {
            strptime(arg, "%Y-%m-%d %H:%M", &dts);
        }
        // 17-09-14 10:29:40
        else if ( strlen(arg) == 17 )
        {
            strptime(arg, "%y-%m-%d %H:%M:%S", &dts);
        }
        // 2017-09-14 10:29:40
        else if ( strlen(arg) == 19 )
        {
            strptime(arg, "%Y-%m-%d %H:%M:%S", &dts);
        }
        else
        {
            fprintf(stderr, "Invalid date '%s' (%lu bytes)\n", arg, strlen(arg));
            throw 3;
        }
        strftime(odate_iata, iata_len, "%d%b%Y", &dts);
        strftime(odate_mdy, mdy_len, "%m/%d/%Y", &dts);
    }
    printf("Date %s (%s)", odate_mdy, odate_iata);
    return 0;
} // MakeFlightDate()


/**
 * Convert date
 *
 * @param idate     input date
 * @param odate     output buffer
 *
 * @return zero upon success otherwise non-zero
 */
int MakeFlightDate(const char * idate,
                   char * odate)
{
    int month_no=0;
    char monst[8]={0};
    std::string month_str;

    //    12/13/2014
    if (!( idate[2] == '/' && idate[5] == '/' && strlen(idate)==10 ))
    {
        fprintf(stderr, "Invalid date %s\n", idate);
        strcpy(odate, idate);
        return -1;
    }

    monst[0] = idate[0];
    monst[1] = idate[1];
    monst[2] = 0;
    month_no = atoi(monst);
    switch ( month_no )
    {
        case 1  :
            month_str = "JAN";
            break;
        case 2 :
            month_str = "FEB";
            break;
        case 3 :
            month_str = "MAR";
            break;
        case 4 :
            month_str = "APR";
            break;
        case 5 :
            month_str = "MAY";
            break;
        case 6 :
            month_str = "JUN";
            break;
        case 7 :
            month_str = "JUL";
            break;
        case 8 :
            month_str = "AUG";
            break;
        case 9 :
            month_str = "SEP";
            break;
        case 10 :
            month_str = "OCT";
            break;
        case 11 :
            month_str = "NOV";
            break;
        case 12 :
            month_str = "DEC";
            break;
        default :
            fprintf(stderr, "Invalid month %s", monst);
    }
    sprintf(odate, "%c%c%3s%c%c", idate[3], idate[4], month_str.c_str(), idate[8], idate[9]);

    return 0;
} // MakeFlightDate()

// Constructor
WriteSsmData::WriteSsmData(std::string aftype,
                           std::string aAddress,
                           std::string aSender,
                           std::string aTimeMode,
                           std::string aFlightNumber,
                           std::string aFlightDateStart,
                           std::string aFlightDateEnd,
                           std::string aDepartCity,
                           int aDepartTime,
                           std::string aArriveCity,
                           int aArriveTime,
                           std::string aAircraftCode,
                           int aFrequencyCode,
                           std::string aCodeshare,
                           std::string aTailNumber)
{
    std::ostringstream ss;

    ftype = aftype;
    Address = aAddress;
    Sender = aSender;
    TimeMode = aTimeMode;
    FlightNumber = aFlightNumber;
    FlightDateStart = aFlightDateStart;
    FlightDateEnd = aFlightDateEnd;
    DepartCity = aDepartCity;
    if ( verbose>=2 ) fprintf(stderr, "Depart %s\n", DepartCity.c_str());

    ss.clear();
    ss.str("");
    ss << std::setfill('0') << std::setw(4) << aDepartTime;
    DepartTime = ss.str();
    if ( verbose>=2 ) fprintf(stderr, "Depart time '%s'\n", DepartTime.c_str());

    ArriveCity = aArriveCity;
    if ( verbose>=2 ) fprintf(stderr, "Arrive %s\n", ArriveCity.c_str());

    ss.clear();
    ss.str("");
    ss << std::setfill('0') << std::setw(4) << aArriveTime;
    ArriveTime = ss.str();
    if ( verbose>=2 ) fprintf(stderr, "Arrive time '%s'\n", ArriveTime.c_str());

    AircraftCode = aAircraftCode;
    if ( verbose>=2 ) fprintf(stderr, "Aircraft code '%s'\n", AircraftCode.c_str());

    ss.clear();
    ss.str("");
    ss << std::setw(0) << aFrequencyCode;
    FrequencyCode = ss.str();
    if ( verbose>=2 ) fprintf(stderr, "Frequency '%s'\n", FrequencyCode.c_str());

    Codeshare = aCodeshare;
    if ( verbose>=2 ) fprintf(stderr, "Codeshare '%s'\n", Codeshare.c_str());

    if ( AircraftCode == "733" )
    {
        SeatCount = "Y144";
        BookingClasses = "YZAUSBMPDITHQVWLXRNGEFKJO144";
        //?TailNumber = "ZSDRI";
    }
    else if ( AircraftCode == "738" )
    {
        SeatCount = "C2Y186";
        BookingClasses = "C002YZAUSBMPDITHQVWLXRNGEFKJO186";
        //?TailNumber = "ZSAGT";
    }
    else if ( AircraftCode == "320" )
    {
        SeatCount = "Y180";
        BookingClasses = "YZAUSBMPDITHQVWLXRNGEFKJO177";
        //?TailNumber = "ZSAXX";
    }
    else if ( ftype == "CNL" )
    {
        // No aircraft code needed here
        SeatCount.clear();
        BookingClasses.clear();
        //?TailNumber.clear();
    }
    else
    {
        fprintf(stderr, "Unknown aircraft code '%s'\n", AircraftCode.c_str());
        throw 1;
    }

    if ( aTailNumber.empty() && aftype != "CNL" )
    {
        TailNumber = "ZS";
        TailNumber += DepartCity.at(0);
        TailNumber += ArriveCity.at(0);
        TailNumber += (aDepartTime/100)+65;
    }
    else
    {
        TailNumber = aTailNumber;
    }

    /*?
    if ( MakeFlightDate(FlightDateStart.c_str(), date1) )
    {
        throw 2;
    }
    if ( verbose>=2 ) fprintf(stderr, "Start %s\n", date1);

    if ( MakeFlightDate(FlightDateEnd.c_str(), date2) )
    {
        throw 3;
    }
    ?*/

    try
    {
        SsmDate sdate(FlightDateStart);
        SsmDate edate(FlightDateEnd);

        if ( FrequencyCode.find(sdate.dow+48) == std::string::npos )
        {
            fprintf(stderr, "Start %s day of week %d not in frequency %s\n",
                    sdate.iata, sdate.dow, FrequencyCode.c_str());
            throw 2;
        }

        if ( FrequencyCode.find(edate.dow+48) == std::string::npos )
        {
            fprintf(stderr, "End %s day of week %d not in frequency %s\n",
                    edate.iata, edate.dow, FrequencyCode.c_str());
            throw 2;
        }

        if ( FrequencyCode.find(sdate.dow+48) == std::string::npos )
        {
            fprintf(stderr, "Start %s day of week %d not in frequency %s",
                    sdate.iata, sdate.dow, FrequencyCode.c_str());
            throw 2;
        }

        strcpy(date1, sdate.iata);
        strcpy(date2, edate.iata);
    }
    catch ( ... )
    {
        fprintf(stderr, "Some sort of date error\n");
        throw 1;
    }
    if ( verbose>=2 ) fprintf(stderr, "Start %s end %s\n", date1, date2);

    now = time(0);   // get time now
    if ( TimeMode == "LT" )
    {
        nowstruct = localtime(&now);
    }
    else if ( TimeMode == "UTC" )
    {
        nowstruct = gmtime(&now);
    }
    else
    {
        fprintf(stderr, "Invalid time mode %s\n", TimeMode.c_str());
        throw 4;
    }
    sprintf(timenow, "%02d%02d%02d", nowstruct->tm_hour, nowstruct->tm_min, nowstruct->tm_sec);
    if ( verbose>=2 ) fprintf(stderr, "Time is %s\n", timenow);
} // WriteSsmData::WriteSsmData()


// Destructor
WriteSsmData::~WriteSsmData()
{
    ;
} // WriteSsmData::~WriteSsmData()


// Write cancel SSM
void WriteSsmData::WriteCnl()
{
    obuff = Address + "\n"
            + "." + Sender + " " + timenow + "\n"
            + "SSM\n"
            + TimeMode + "\n"
            + "CNL\n"
            + FlightNumber + "\n"
            + date1 + " " + date2 + " " + FrequencyCode + "\n";
    /// @todo is this legit?
    /*
    if ( Codeshare.size() )
    {
        obuff = obuff + DepartCity + ArriveCity + " 10/" + Codeshare + "\n";
    }
    ?*/
} // WriteSsmData::WriteCnl()


// Write equipment SSM
void WriteSsmData::WriteEqt()
{
    obuff = Address + "\n"
            + "." + Sender + " " + timenow + "\n"
            + "SSM\n"
            + TimeMode + "\n"
            + "EQT\n"
            + FlightNumber + "\n"
            + date1 + " " + date2 + " " + FrequencyCode + "\n"
            + "J " + AircraftCode + " XX." + SeatCount + " " + TailNumber + "\n"
            + "QQQQQQ 106/" + BookingClasses + "\n";
} // WriteSsmData::WriteEqt()


// Write new flight SSM
void WriteSsmData::WriteNew()
{
    obuff = Address + "\n"
            + "." + Sender + " " + timenow + "\n"
            + "SSM\n"
            + TimeMode + "\n"
            + "NEW\n"
            + FlightNumber + "\n"
            + date1 + " " + date2 + " " + FrequencyCode + "\n"
            + "J " + AircraftCode + " XX." + SeatCount + " " + TailNumber + "\n"
            + DepartCity + DepartTime + " " + ArriveCity + ArriveTime + " 7\n" /// @todo 7??
            + DepartCity + ArriveCity + " 8/A\n"
            + DepartCity + ArriveCity + " 99/0\n";
    if ( Codeshare.size() )
    {
        obuff = obuff + DepartCity + ArriveCity + " 10/" + Codeshare + "\n";
    }
    if ( AircraftCode == "738" )
    {
        obuff = obuff + DepartCity + ArriveCity + " 106/C002YZAUSBMPDITHQVWLXRNGEFKJO186\n";
    }
    else if ( AircraftCode == "733" )
    {
        obuff = obuff + DepartCity + ArriveCity + " 106/YZAUSBMPDITHQVWLXRNGEFKJO144";
    }
    else if ( AircraftCode == "320" )
    {
        obuff = obuff + DepartCity + ArriveCity + " 106/YZAUSBMPDITHQVWLXRNGEFKJO177";
    }
    else
    {
        /// @todo something
        ;
    }
} // WriteSsmData::WriteNew()


// Write replace flight SSM
void WriteSsmData::WriteRpl()
{
    obuff = Address + "\n"
            + "." + Sender + " " + timenow + "\n"
            + "SSM\n"
            + TimeMode + "\n"
            + "RPL\n"
            + FlightNumber + "\n"
            + date1 + " " + date2 + " " + FrequencyCode + "\n"
            + "J " + AircraftCode + " XX." + SeatCount + " " + TailNumber + "\n"
            + DepartCity + DepartTime + " " + ArriveCity + ArriveTime + " 7\n" /// @todo 7??
            + DepartCity + ArriveCity + " 106/" + BookingClasses + "\n";
    if ( Codeshare.size() )
    {
        obuff = obuff + DepartCity + ArriveCity + " 10/" + Codeshare + "\n";
    }
} // WriteSsmData::WriteRpl()


// Write time change SSM
void WriteSsmData::WriteTim()
{
    obuff = Address + "\n"
            + "." + Sender + " " + timenow + "\n"
            + "SSM\n"
            + TimeMode + "\n"
            + "TIM\n"
            + FlightNumber + "\n"
            + date1 + " " + date2 + " " + FrequencyCode + "\n"
            + DepartCity + DepartTime + " " + ArriveCity + ArriveTime + "\n";
} // WriteSsmData::WriteTim()


std::string WriteSsmData::FileName()
{
    std::string fname;

    fname = IntToRoman(atoi(FlightNumber.substr(2).c_str())) + FlightDateStart + ftype + FlightDateEnd;

    return fname;
}

// Write SSM file
int WriteSsmData::WriteSsmFile(std::string ofname)
{
    FILE * ofile;
    int rv=0;

    if ( ftype == "CNL" )
    {
        WriteCnl();
    }
    else if ( ftype == "EQT" )
    {
        WriteEqt();
    }
    else if ( ftype == "NEW" )
    {
        WriteNew();
    }
    else if ( ftype == "RPL" )
    {
        WriteRpl();
    }
    else if ( ftype == "TIM" )
    {
        WriteTim();
    }
    else
    {
        fprintf(stderr, "Unknown file type '%s'", ftype.c_str());
        throw 11;
    }
    obuff += "\n";

    if ( ofname.empty() ) ofname = "-";

    if ( ofname != "-" )
    {
        if ( verbose>=2 ) fprintf(stderr, "Write output file %s\n", ofname.c_str());
        ofile = fopen(ofname.c_str(), "w");
        if (! ofile)
        {
            fprintf(stderr, "Could not write %s\n", ofname.c_str());
            throw 10;
        }
        obuff += "\03\03\n";
        fprintf(ofile, "%s", obuff.c_str());
        fclose(ofile);
    }
    else
    {
        printf("%s", obuff.c_str());
    }

    return rv;
} // WriteSsmData::WriteSsmFile()
