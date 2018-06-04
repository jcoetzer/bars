/**
 * @file SsmDate.cpp
 *
 * Read date in any format and convert
 */

#include <map>
#include <string>

#include <string.h>
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>

// #include "SsmDb.h"
#include "SsmUtils.h"
#include "SsmDate.h"
#include "SsmDate.hpp"
#include "UserLogSsm.h"


/*
 * Get day of week
 * 1 for Monday, 7 for Sunday etc.
 */
int DayOfWeek(int y, int m, int d)
{
    static int t[] = {0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4};
    int rc;

    y -= m < 3;
    // value is 0 = Sunday, 1 = Monday, etc.
    rc = (y + y/4 - y/100 + y/400 + t[m-1] + d) % 7;
    if ( rc==0 ) rc = 7;
    return rc;
} // DayOfWeek()

// Write time to log
void TimeStamp(const char * msg)
{
    time_t now = time(NULL);
    struct tm * tmnow = localtime((const time_t *)&now);

    userlogv(1, "%02d:%02d:%02d %s",
             tmnow->tm_hour, tmnow->tm_min, tmnow->tm_sec, msg);
    fflush(ssmlog);
} // TimeStamp()


// Write date and time to log
void DateTimeStamp(const char * msg)
{
    time_t now = time(NULL);
    struct tm * tmnow = localtime((const time_t *)&now);

    userlogv(1, "%04d-%02d-%02d %02d:%02d:%02d %s",
             tmnow->tm_year+1900, tmnow->tm_mon+1, tmnow->tm_mday,
             tmnow->tm_hour, tmnow->tm_min, tmnow->tm_sec, msg);
    fflush(ssmlog);
} // TimeStamp()


// Date time in format yyyymmddThhmmss for use in log file name
char * GetDateTimeStamp()
{
    static char rbuf[64];
    time_t now = time(NULL);
    struct tm * tmnow = localtime((const time_t *)&now);

    snprintf(rbuf, sizeof(rbuf), "%04d%02d%02dT%02d%02d%02d",
             tmnow->tm_year+1900, tmnow->tm_mon+1, tmnow->tm_mday,
             tmnow->tm_hour, tmnow->tm_min, tmnow->tm_sec);

    return rbuf;
} // GetDateTimeStamp()


// Constructor
SsmDate::SsmDate(long adate)
{
    strcpy(mdy, "");
    strcpy(iata, "");
} // SsmDate::SsmDate()


// Constructor
SsmDate::SsmDate(char * adate)
{
    char * dtok;
    int m=0, d=0, y=0;

    strcpy(mdy, adate);
    strcpy(iata, adate);
    dtok = strtok(iata, "/");
    if ( dtok )
    {
        m = atoi(dtok);
        dtok = strtok(NULL, "/");
        if ( dtok )
        {
            d = atoi(dtok);
            dtok = strtok(NULL, "/");
            if ( dtok )
            {
                y = atoi(dtok);
            }
        }
    }

    switch ( m )
    {
        case 1  :
            sprintf(iatal, "%02dJAN%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 2 :
            sprintf(iatal, "%02dFEB%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 3 :
            sprintf(iatal, "%02dMAR%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 4 :
            sprintf(iatal, "%02dAPR%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 5 :
            sprintf(iatal, "%02dMAY%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 6 :
            sprintf(iatal, "%02dJUN%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 7 :
            sprintf(iatal, "%02dJUL%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 8 :
            sprintf(iatal, "%02dAUG%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 9 :
            sprintf(iatal, "%02dSEP%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 10 :
            sprintf(iatal, "%02dOCT%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 11 :
            sprintf(iatal, "%02dNOV%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        case 12 :
            sprintf(iatal, "%02dDEC%04d", d, y);
            sprintf(iata, "%02dJAN%02d", d, y%100);
            break;
        default :
            strcpy(iata, adate);
    }
    sprintf(mdy, "%02d/%02d/%04d", m, d, y);
    sprintf(iso, "%04d-%02d-%02d", y, m, d);

    dow = DayOfWeek(y, m, d);
} // SsmDate::SsmDate()


// Constructor
SsmDate::SsmDate(std::string datev)
{
    long idate;
    struct tm dts;
    char arg[64];
    time_t now;
    struct tm * dtnow;
    char dowst[4];

    if ( datev.empty() )
    {
        fprintf(stderr, "Empty date\n");
        throw 1;
    }

    strcpy(arg, datev.c_str());
    now = time(NULL);

    if ( 0 == strcasecmp(arg, "yesterday") )
    {
        now -= 24*60*60;
        dtnow = localtime(&now);
        dts.tm_sec  = dtnow->tm_sec;         /* seconds */
        dts.tm_min  = dtnow->tm_min;         /* minutes */
        dts.tm_hour = dtnow->tm_hour;        /* hours */
        dts.tm_mday = dtnow->tm_mday;        /* day of the month */
        dts.tm_mon  = dtnow->tm_mon;         /* month */
        dts.tm_year = dtnow->tm_year;        /* year */
        dts.tm_wday = dtnow->tm_wday;        /* day of the week */
        dts.tm_yday = dtnow->tm_yday;        /* day in the year */
        dts.tm_isdst= dtnow->tm_isdst;       /* daylight saving time */
    }
    else if ( 0 == strcasecmp(arg, "today") )
    {
        dtnow = localtime(&now);
        dts.tm_sec  = dtnow->tm_sec;         /* seconds */
        dts.tm_min  = dtnow->tm_min;         /* minutes */
        dts.tm_hour = dtnow->tm_hour;        /* hours */
        dts.tm_mday = dtnow->tm_mday;        /* day of the month */
        dts.tm_mon  = dtnow->tm_mon;         /* month */
        dts.tm_year = dtnow->tm_year;        /* year */
        dts.tm_wday = dtnow->tm_wday;        /* day of the week */
        dts.tm_yday = dtnow->tm_yday;        /* day in the year */
        dts.tm_isdst= dtnow->tm_isdst;       /* daylight saving time */
    }
    else if ( 0 == strcasecmp(arg, "tomorrow") )
    {
        now += 24*60*60;
        dtnow = localtime(&now);
        dts.tm_sec  = dtnow->tm_sec;         /* seconds */
        dts.tm_min  = dtnow->tm_min;         /* minutes */
        dts.tm_hour = dtnow->tm_hour;        /* hours */
        dts.tm_mday = dtnow->tm_mday;        /* day of the month */
        dts.tm_mon  = dtnow->tm_mon;         /* month */
        dts.tm_year = dtnow->tm_year;        /* year */
        dts.tm_wday = dtnow->tm_wday;        /* day of the week */
        dts.tm_yday = dtnow->tm_yday;        /* day in the year */
        dts.tm_isdst= dtnow->tm_isdst;       /* daylight saving time */
    }
    else
    {
        memset(&dts, 0, sizeof(struct tm));
        // 20JUL
        if ( strlen(arg) == 5 )
        {
            strptime(arg, "%d%b", &dts);
            // Use current year
            dtnow = localtime(&now);
            dts.tm_year = dtnow->tm_year;
        }
        // 20JUL17
        else if ( strlen(arg) == 7 )
        {
            strptime(arg, "%d%b%y", &dts);
        }
        // 20170720
        else if ( strlen(arg) == 7 )
        {
            strptime(arg, "%Y%m%d", &dts);
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
    }
    strftime(iatal, sizeof(iatal), "%d%b%Y", &dts);
    iatal[3] = toupper(iatal[3]);
    iatal[4] = toupper(iatal[4]);
    strftime(iata, sizeof(iata), "%d%b%y", &dts);
    iata[3] = toupper(iata[3]);
    iata[4] = toupper(iata[4]);
    strftime(mdy, sizeof(mdy), "%m/%d/%Y", &dts);
    strftime(iso, sizeof(iso), "%Y-%m-%d", &dts);
    strftime(dowst, sizeof(dowst), "%w", &dts);
    dow = atoi(dowst);
    if ( dow == 0 ) dow = 7;
    //? userlogv(3, "Date %s (%s)", mdy, iata);
} // SsmDate::SsmDate()


// Destructor
SsmDate::~SsmDate()
{
    ;
} // SsmDate::~SsmDate()


