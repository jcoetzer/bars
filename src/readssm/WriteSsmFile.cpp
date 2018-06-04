/**
 * @file WriteSsmFile.cpp
 *
 * Write SSM message for testing
 */
#include <string>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <libgen.h>
#include <stdio.h>
#include <string.h>

#include "gitrev.h"
#include "SsmUtils.h"
#include "SsmData.h"
#include "UserLogSsm.h"
#include "CheckFlight.h"
#include "ReadCsvData.h"

#include "WriteSsm.h"

extern char * yytext;

long SsmTimeZone = 200L;

int verbose = 1;
FILE * ssmlog;

/**
 * Display help message
 *
 * @param pname     file name
 */
void show_usage(char * pname);

/**
 * Display build information
 *
 * @param pname     file name
 */
void show_version(char * pname);


/**
 * The big cheese
 *
 * @param argc number of arguments
 * @param argv argument values
 *
 * @return zero upon success otherwise non-zero
 */
int main(int argc, char **argv)
{
    int i, rc;
    std::string ifname, ofname, ftype;
    std::string FlightNumber;
    std::string FlightDateStart;
    std::string FlightDate;
    std::string FlightDateEnd;
    std::string AircraftCode;
    std::string TailNumber;
    int FrequencyCode=0, FrequencyCode1=0, FrequencyCode2=0;
    std::string Address;
    std::string Sender;
    std::string DepartCity;
    int DepartTime = 0;
    std::string ArriveCity;
    int ArriveTime = 0;
    std::string TimeMode;
    std::string Codeshare;

    ssmlog = stdout;

    ifname.clear();
    ofname.clear();
    ftype.clear();
    FlightNumber.clear();
    DepartCity.clear();
    ArriveCity.clear();
    FlightDateStart.clear();
    FlightDateEnd.clear();
    Codeshare.clear();
    AircraftCode.clear();
    TailNumber.clear();

    Address = "QK SWITT1G";
    Sender = "JNB7ASA";
    TimeMode = "LT";

    verbose = 1;
    ftype = "CNL";

    i = 1;
    rc = argc;
    while (i < argc)
    {
        if ( 0 == strcmp(argv[i], "-h") || 0 == strncmp(argv[i], "--h", 3) )
        {
            show_usage(argv[0]);
        }
        else if ( 0 == strncmp(argv[i], "--v", 3) )
        {
            show_version(argv[0]);
        }
        else if ( 0 == strcmp(argv[i], "-V") )
        {
            verbose = 3;
        }
        else if ( 0 == strcmp(argv[i], "-v") )
        {
            verbose = 2;
        }
        else if ( 0 == strcmp(argv[i], "--cnl") )
        {
            ftype = "CNL";
        }
        else if ( 0 == strcmp(argv[i], "--csv") )
        {
            ifname = "-";
        }
        else if ( 0 == strcmp(argv[i], "--eqt") )
        {
            ftype = "EQT";
        }
        else if ( 0 == strcmp(argv[i], "--new") )
        {
            ftype = "NEW";
        }
        else if ( 0 == strcmp(argv[i], "--rpl") )
        {
            ftype = "RPL";
        }
        else if ( 0 == strcmp(argv[i], "--tim") )
        {
            ftype = "TIM";
        }
        else if ( 0 == strcmp(argv[i], "--utc") )
        {
            TimeMode = "UTC";
        }
        else if ( 0 == strcmp(argv[i], "-A") )
        {
            ++i;
            AircraftCode = std::string(argv[i]);
        }
        else if ( 0 == strcmp(argv[i], "-D") )
        {
            ++i;
            FlightDateStart = std::string(argv[i]);
        }
        else if ( 0 == strcmp(argv[i], "-E") )
        {
            ++i;
            FlightDateEnd = std::string(argv[i]);
        }
        else if ( 0 == strcmp(argv[i], "-F") )
        {
            ++i;
            FlightNumber = std::string(argv[i]);
        }
        else if ( 0 == strcmp(argv[i], "-G") )
        {
            ++i;
            Codeshare = std::string(argv[i]);
        }
        else if ( 0 == strcmp(argv[i], "-I") )
        {
            ++i;
            ifname = std::string(argv[i]);
        }
        else if ( 0 == strcmp(argv[i], "-K") )
        {
            ++i;
            FrequencyCode = atoi(argv[i]);
        }
        else if ( 0 == strcmp(argv[i], "-P") )
        {
            ++i;
            DepartCity = argv[i];
        }
        else if ( 0 == strcmp(argv[i], "-Q") )
        {
            ++i;
            ArriveCity = argv[i];
        }
        else if ( 0 == strcmp(argv[i], "-T") )
        {
            ++i;
            TailNumber = argv[i];
        }
        else if ( 0 == strcmp(argv[i], "-X") )
        {
            ++i;
            if ( strlen(argv[i])==5 && argv[i][2]==':' )
            {
                DepartTime = atoi(&argv[i][3]);
                argv[i][2] = 0;
                DepartTime += atoi(argv[i])*100;
            }
            else
            {
                DepartTime = atoi(argv[i]);
            }
        }
        else if ( 0 == strcmp(argv[i], "-Y") )
        {
            ++i;
            if ( strlen(argv[i])==5 && argv[i][2]==':' )
            {
                ArriveTime = atoi(&argv[i][3]);
                argv[i][2] = 0;
                ArriveTime += atoi(argv[i])*100;
            }
            else
            {
                ArriveTime = atoi(argv[i]);
            }
        }
        else
        {
            ofname = argv[i];
        }
        ++i;
    }

    if ( ftype.empty() )
    {
        fprintf(stderr, "File type not specified\n");
        return -1;
    }

    if ( ofname.empty() )
    {
        ofname = "-";
    }

    // if ( ifname.empty() )
    // {
    //     ifname = "-";
    // }

    if ( 0 == ArriveTime )
    {
        ArriveTime = DepartTime + 200;
    }

    if ( TimeMode == "UTC" )
    {
        DepartTime -= SsmTimeZone;
        if ( DepartTime < 0 )
        {
            DepartTime += 2400;
            fprintf(stderr, "Departure time %04d is too complicated\n", DepartTime);
            return -1;
        }
        ArriveTime -= SsmTimeZone;
        if ( ArriveTime < 0 )
        {
            ArriveTime += 2400;
            fprintf(stderr, "Arrival time %04d is too complicated\n", ArriveTime);
            return -1;
        }
    }

    if ( FlightNumber.size() && FlightDateStart.size() )
    {
        if ( FlightDateEnd.empty() )
        {
            FlightDateEnd = FlightDateStart;
            //? FrequencyCode = DayOfWeek((char*)FlightDateEnd.c_str());
        }
        if ( 0 == FrequencyCode )
        {
            FrequencyCode1 = DayOfWeekSt((char*)FlightDateStart.c_str());
            if ( FlightDateStart != FlightDateEnd )
            {
                FrequencyCode2 = DayOfWeekSt((char*)FlightDateEnd.c_str());
                if ( FrequencyCode1 <= FrequencyCode2 )
                {
                    FrequencyCode = 10*FrequencyCode1+FrequencyCode2;
                }
                else
                {
                    FrequencyCode = 10*FrequencyCode2+FrequencyCode1;
                }
            }
            else
            {
                FrequencyCode = FrequencyCode1;
            }
        }
        if ( ftype == "NEW" || ftype == "TIM" )
        {
            if ( DepartCity.empty() )
            {
                fprintf(stderr, "Departure not specified for %s\n", ftype.c_str());
                return -1;
            }
            if ( ArriveCity.empty() )
            {
                fprintf(stderr, "Arrival not specified for %s\n", ftype.c_str());
                return -1;
            }
            if ( 0==DepartTime && 0==ArriveTime )
            {
                fprintf(stderr, "Departure and/or arrival time not specified for %s\n", ftype.c_str());
                return -1;
            }
            if ( AircraftCode.empty() )
            {
                fprintf(stderr, "Aircraft code not specified for %s\n", ftype.c_str());
                return -1;
            }
        }
        else if ( ftype == "EQT" )
        {
            if ( AircraftCode.empty() )
            {
                fprintf(stderr, "Aircraft code not specified for %s\n", ftype.c_str());
                return -1;
            }
        }
        else
        {
            // All is well
            ;
        }
        try
        {
            WriteSsmData ssmData = WriteSsmData(ftype, Address, Sender, TimeMode,
                                                FlightNumber, FlightDateStart, FlightDateEnd,
                                                DepartCity, DepartTime, ArriveCity, ArriveTime,
                                                AircraftCode, FrequencyCode, Codeshare, TailNumber);
            ssmData.WriteSsmFile(ofname);
        }
        catch ( ... )
        {
            fprintf(stderr, "Processing error\n");
            rc = -1;
        }
    }
    else
    {
        fprintf(stderr, "Flight number, date and frequency must be specified\n");
    }

    return rc;
} // main()


// Display build information
void show_version(char * pname)
{
    fprintf(stderr, "%s :\n", basename(pname));
    fprintf(stderr, "\tWrite flight data (version %s) %s\n", gitrev, dtbuild);
    exit(1);
} // show_version()


// Display help message
void show_usage(char * pname)
{
    fprintf(stderr, "Write flight data (version %s) :\n", gitrev);
    fprintf(stderr, "\t%s --cnl|--eqt|--new|--rpl|--tim\n", basename(pname));
    fprintf(stderr, "\t\t -F <FLIGHT> -D <DATE> -Q <FREQ>\n");
    fprintf(stderr, "\t\t [-E <DATE>] [-A <CODE>] [-I <TIME>] [-J <TIME>] [-K <CITY>] [-L <CITY>] [-G <FLIGHT>] [-T <TAIL>]\n");
    fprintf(stderr, "\t\t <FILE>\n");
    fprintf(stderr, "where\n");
    fprintf(stderr, "\t-v\t\t Additional output\n");
    fprintf(stderr, "\t--cnl\t\t Cancel flight\n");
    fprintf(stderr, "\t--eqt\t\t Equipment change\n");
    fprintf(stderr, "\t--new\t\t New flight\n");
    fprintf(stderr, "\t--rpl\t\t Replace flight\n");
    fprintf(stderr, "\t--tim\t\t Time change\n");
    fprintf(stderr, "\t--utc\t\t Time zone UTC (default is LT)\n");
    fprintf(stderr, "\t-A <CODE>\t Aircraft code, e.g. 738\n");
    fprintf(stderr, "\t-F <FLIGHT>\t Flight number, e.g. JE123\n");
    fprintf(stderr, "\t-G <FLIGHT>\t Codeshare flight number, e.g SA2164\n");
    fprintf(stderr, "\t-D <DATE>\t Start date, e.g. 11/06/2018\n");
    fprintf(stderr, "\t-E <DATE>\t End date, e.g. 11/26/2018\n");
    fprintf(stderr, "\t-K <FREQ>\t Frequency code, e.g. 34\n");
    fprintf(stderr, "\t-P <CITY>\t Departure airport, e.g. JNB\n");
    fprintf(stderr, "\t-Q <CITY>\t Arrival airport, e.g. GRJ\n");
    fprintf(stderr, "\t-T <TAIL>\t Tail number\n");
    fprintf(stderr, "\t-X <TIME>\t Departure time, e.g. 1120\n");
    fprintf(stderr, "\t-Y <TIME>\t Arrival time, e.g. 1325\n");
    fprintf(stderr, "\t<FILE>\t\t Output file name (specify '-' for standard output)\n");
    //?fprintf(stderr, "\t<IFILE>\t\tOutput file name (default is standard input)\n");
    exit(1);
} // show_usage()
