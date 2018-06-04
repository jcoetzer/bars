/**
 * @file SsmUtils.cpp
 *
 * Support functions
 */
#include <vector>
#include <string>
#include <ctime>

#include <string.h>
#include <time.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#include "UserLogSsm.h"
#include "SsmUtils.h"
//? #include "SsmDb.h"

#define NOTUX 1
#include "UserLogSsm.h"

/*
 * Trim trailing spaces
 */
std::string& rtrim(std::string& s,
                   const char* t)
{
    s.erase(s.find_last_not_of(t) + 1);
    return s;
} // rtrim()


/*
 * Create timestamp
 */
char * crea_date_time(char* create_dts)
{
    static char dts[32] = {0};
    time_t secs = time(NULL);
    struct tm * time_now = localtime(&secs);

    sprintf(dts, "%04d/%02d/%02d/%02d/%02d/%02d",
            time_now->tm_year+1900, time_now->tm_mon+1, time_now->tm_mday,
            time_now->tm_hour, time_now->tm_min, time_now->tm_sec);
    if ( create_dts ) strcpy(create_dts, dts);
    return dts;
} // crea_date_time()


/*
 * Create timestamp
 */
char * crea_date_time_iso()
{
    static char create_dts[32];
    time_t secs = time(NULL);
    struct tm * time_now = localtime(&secs);

    sprintf(create_dts, "%04d-%02d-%02d %02d:%02d:%02d",
            time_now->tm_year+1900, time_now->tm_mon+1, time_now->tm_mday,
            time_now->tm_hour, time_now->tm_min, time_now->tm_sec);
    return create_dts;
} // crea_date_time_iso()


/*
 * Strip any trailing whitespace from a string
 */
extern "C"
char * strrtrim(char * string)
{
    if ( string != NULL )
    {
        /* Get a pointer to the last char in the string */
        char *tempStr = string + strlen(string) - 1;

        while ( tempStr >= string && isspace(*tempStr) )
        {
            *tempStr = '\0';
            tempStr--;
        }
    }

    return string;
} // strrtrim()


/*
 * Get database error message
 */
int getDBErrorStringFromNumber(int finderrNo,
                               char *text)
{
    int iretval = 1;

    if ( finderrNo != 0 && text != NULL )
    {
        switch ( finderrNo )
        {
            case -1204:
                strcpy(text, "YEAR");
                break;
            case -1205:
                strcpy(text, "MONTH");
                break;
            case -1206:
                strcpy(text, "DAY");
                break;
            case -1212:
                strcpy(text, "DATE FROMAT");
                break;
            case -1218:
                strcpy(text, "NOT DATE");
                break;
            default:
                strcpy(text, "DATE FORMAT");
        }
        iretval = 0;
    }
    return iretval;
} // getDBErrorStringFromNumber()


/*
 * Convert string to frequency codes
 */
#ifdef __cplusplus
extern "C"
#endif
char * str2freq(char *days,
                int datechg)
{
    static char res[8];
    int i;
    int d;
    int j;
    char freq[10];

    memset(freq, 0, sizeof( freq ));

    for ( j = 0; days[j]; j++ )
    {
        days[j] = days[j] + datechg;
        if ( days[j] == '0' )
        {
            days[j] = '7';
        }
        if ( days[j] == '8' )
        {
            days[j] = '1';
        }
    }

    strcpy(res, "-------");

    for ( i = 0; days[i]; i++ )
    {
        d = days[i] - '1';
        res[d] = days[i];
    }
    return(res);
} // str2freq()


/*
 * Check if frequency is a subset
 */
extern "C"
int isSubset(char *newFrequency,
             char *oldFrequency,
             int *subset)
{
    int iretval = 1;
    int i = 0, j = 0;
    int numberOfDaysMatched = 0, numberOfDaysInNewFreq = 0;

    if ( oldFrequency != NULL && newFrequency != NULL && subset != NULL)
    {
        *subset = 0;

        for ( i = 0; i < 7; i++ )
        {
            if ( newFrequency[i] != '-' )
            {
            numberOfDaysInNewFreq++;
            }
        }

        for ( i = 0; i < 7; i++ )
        {
            if ( newFrequency[i] == '-' )
            {
                continue;
            }

            for( j = 0; j < 7; j++ )
            {
                if ( newFrequency[i] == oldFrequency[j] )
                {
                    numberOfDaysMatched++;
                    if ( numberOfDaysMatched == numberOfDaysInNewFreq)
                    {
                        userlog("New %s is a subset of old %s", newFrequency, oldFrequency);
                        *subset = 1;
                        break;
                    }
                }
            } // end all oldFrequency chars
        } // end for one char of newFrequency at the time
        iretval = 0;
    }  // end if valid data passed in

   return iretval;
} // isSubset()


/*
 * Set up new frequencies
 *
 */
extern "C"
int differentiateFrequencies(char *newFrequency,
                             char *oldFrequencyToChange,
                             int oldFrequencyToChangeSize)
{
    int i = 0;
    int iretval = 1;

    if ( newFrequency != NULL && oldFrequencyToChange != NULL )
    {
        for ( i=0; newFrequency[i] != '\0'; i++ )
        {
            if ( newFrequency[i] != '-' )
            {
                oldFrequencyToChange[i] = '-';
            }
        }
        iretval = 0;
    }
    userlog("Differentiated frequencies from %s to %s", newFrequency, oldFrequencyToChange);
    return iretval;
} // differentiateFrequencies()


/*
 * Get some sort of intersection
 */
extern "C"
int getSetIntersect(struct FlightData * pFlightDataPtr)
{
    int iretval = 1;
    int k = 0, j = 0, i = 0;
    char diffFreqCode[16] = {0};

    for ( k = 0 ; k < 7; k++ )
    {
        for ( j = 0; j < 7; j++)
        {
            if ( pFlightDataPtr->oldFrequencyCode[k] == pFlightDataPtr->newFrequencyCode[j] )
            {
                diffFreqCode[i++] = pFlightDataPtr->oldFrequencyCode[k];
                break;
            }
        }
    }
    strcpy(pFlightDataPtr->diffFrequencyCode, str2freq((char *) diffFreqCode, 0));
    userlog("Differentiated frequency set to %s", pFlightDataPtr->diffFrequencyCode);
    iretval = 0;

    return iretval;
} // getSetIntersect()


/*
 * Get frequencies for split flight
 */
extern "C"
int getFrequenciesForSplit(struct FlightData * pFlightDataPtr,
                           int *setIntersect)
{
    int iretval = 1;
    char tempOldFreq[8] = {0};

    strcpy(pFlightDataPtr->diffFrequencyCode,pFlightDataPtr->oldFrequencyCode );
    differentiateFrequencies(pFlightDataPtr->newFrequencyCode,
                             pFlightDataPtr->diffFrequencyCode,
                             sizeof(pFlightDataPtr->diffFrequencyCode ));

    if ( strcmp(pFlightDataPtr->diffFrequencyCode, "-------") != 0 )
    {
        // assign what should be the new OLD frequency for split
        strcpy(tempOldFreq, pFlightDataPtr->diffFrequencyCode);
        // get what should be the new NEW frequency for split
        getSetIntersect(pFlightDataPtr);

        if ( strcmp(pFlightDataPtr->diffFrequencyCode, "-------") == 0 )
        {
            // dates and frequency the same
            return iretval;
        }

        if ( strcmp(pFlightDataPtr->diffFrequencyCode, "-------") != 0
             && strcmp(pFlightDataPtr->oldFrequencyCode, pFlightDataPtr->diffFrequencyCode ) != 0 )
        {
            strcpy(pFlightDataPtr->newFrequencyCode, pFlightDataPtr->diffFrequencyCode);
            strcpy(pFlightDataPtr->oldFrequencyCode, tempOldFreq);
            *setIntersect = 1;
        }
        iretval = 0;
    }

    return iretval;
} // getFrequenciesForSplit()


/*
 * Make path of something or other
 */
#ifdef __cplusplus
extern "C"
#endif
char * mk_path(struct IT ** it,
               const int n_it)
{
    static char res[135 + 1];
    int i;

    res[0] = '\0';
    for ( i = 0; i < n_it; i++ )
    {
        if ( i > 0 )
        {
            strcat(res, "#");
            strcat(res, it[i]->dest);
        }
        else
        {
            sprintf(res, "%s#%s", it[i]->orig, it[i]->dest);
        }
    }
    return res;
} // mk_path()


/*
 * Alter frequency code
 */
extern "C"
int alterFrequency(char *frequency,
                   size_t frequencySize)
{
    int iretval = 1;
    char *whereIsSeven = NULL;

    if ( frequency != NULL && frequencySize == 8 )
    {
        whereIsSeven = strchr(frequency, (int) '7');
        if ( whereIsSeven ) *whereIsSeven = '0';

        iretval = 0;
    }
    return iretval;
} // alterFrequency()


/*
 * Get times and terms for marketed from operational flight
 */
int getTimesTermsForMarketedFromOperational(char *orig,
                                            char *dest,
                                            IT dupfligth,
                                            struct IT ** it,
                                            int cur_it,
                                            size_t depTerminalSize,
                                            size_t arrTerminalSize)
{
    int iretval = 1, i = 0;

    for ( i = 0; i < cur_it; i++ )
    {
        if ( it[i]->orig )
        {
            if ( strncmp (  orig, it[i]->orig, strlen ( it[i]->orig )) == 0 )
            {
                if ( it[i]->depTerminal )
                {
                    strlcpy ( dupfligth.depTerminal, (char *)it[i]->depTerminal, depTerminalSize );
                }
                dupfligth.dep = it[i]->dep;
            }
        }
        if ( it[i]->dest )
        {
            if ( strncmp (  dest, it[i]->dest, strlen ( it[i]->dest )) == 0 )
            {
                if ( it[i]->arrTerminal[0] )
                {
                    strlcpy ( dupfligth.arrTerminal, (char *)it[i]->arrTerminal, arrTerminalSize );
                }
                dupfligth.arr = it[i]->arr;
            }
        }
    }
    iretval = 0;

    return iretval;
} // getTimesTermsForMarketedFromOperational() */


/*
 * Combine frequency codes
 */
extern "C"
int combineFrequencies(char *frequencyCumulator,
                       char *queryFrequencyCode)
{
    int iretval = 1;
    int i = 0;

    if ( frequencyCumulator != NULL && queryFrequencyCode != NULL )
    {
        for ( i = 0; i < 7; i++ )
        {
            if ( queryFrequencyCode[i] != '-' )
            {
                frequencyCumulator[i] = queryFrequencyCode[i] ;
            }
        }
        iretval = 0;
    }
    return iretval;
} // combineFrequencies()


/*
 * Copy src to string dst of size siz.
 */
extern "C"
size_t strlcpy(char * __restrict dst,
               const char * __restrict src,
               size_t siz)
{
    char *d = dst;
    const char *s = src;
    size_t n = siz;

    /* Copy as many bytes as will fit */
    if ( n != 0 )
    {
        while ( --n != 0 )
        {
            if ( (*d++ = *s++) == '\0' ) break;
        }
    }

    /* Not enough room in dst, add NULL and traverse rest of src */
    if ( n == 0 )
    {
        /* NULL-terminate dst */
        if ( siz != 0) *d = '\0';
        while ( *s++ ) ;
    }
    /* count does not include NULL */
    return (s - src - 1);
} // strlcpy()


/*
 * Appends src to string dst of size siz (unlike strncat, siz is the
 * full size of dst, not space left).  At most siz-1 characters
 * will be copied.  Always NUL terminates (unless siz <= strlen(dst)).
 * Returns strlen(src) + MIN(siz, strlen(initial dst)).
 * If retval >= siz, truncation occurred.
 *
 */
size_t strlcat(char *dst, const char *src, size_t siz)
{
    register char *d = dst;
    register const char *s = src;
    register size_t n = siz;
    size_t dlen;

    /* Find the end of dst and adjust bytes left but don't go past end */
    while ( n-- != 0 && *d != '\0' )
    {
        d++;
    }

    dlen = d - dst;
    n = siz - dlen;

    if ( n == 0 )
    {
        return( dlen + strlen(s) );
    }

    while ( *s != '\0' )
    {
        if ( n != 1 )
        {
            *d++ = *s;
            n--;
        }
        s++;
    }
    *d = '\0';

    return (dlen + (s - src));      /* count does not include NUL */
} // strlcat()


/*
 * Return useful stuff
 */
extern "C"
char *dashOut(char *s)
{
    int i = 0, k = 0;
    char tmp[10] = {0};
    int j = strlen(s);

    for( i = 0; i < j;  i++)
    {
        if ( s[i] != '-')
        {
            if ( k <= j )
            {
                tmp[k++] = s[i];
            }
        }
    }
    strlcpy ( s, tmp, j );
    return s;
} // dashOut()


/*
 * Adjust date by a number of days +/-
 */
void DatePlusDays(struct tm* date,
                  int days)
{
    const time_t ONE_DAY = 24 * 60 * 60 ;

    // Seconds since start of epoch
    time_t date_seconds = mktime( date ) + (days * ONE_DAY) ;

    // Update caller's date
    // Use localtime because mktime converts to UTC so may change date
    *date = *localtime( &date_seconds ) ; ;
} // DatePlusDays()


/*
 * Convert date in mdy format to ctime structure
 */
int ConvertDate(char * adate,
                struct tm* vdate)
{
    int year;
    int month;
    int day;
    char * tok;
    char * sdate = strdup(adate);

    /// @todo check for errors here
    tok = strtok(sdate, "/");
    if ( tok == NULL ) return 1;
    month = atoi(tok);

    tok = strtok(NULL, "/");
    if ( tok == NULL ) return 1;
    day = atoi(tok);

    tok = strtok(NULL, "/");
    if ( tok == NULL ) return 1;
    year = atoi(tok);

    // Set up the date structure
    vdate->tm_year = year - 1900 ;
    vdate->tm_mon = month - 1 ;  // note: zero indexed
    vdate->tm_mday = day;
    vdate->tm_hour = 12;
    vdate->tm_min = 0;
    vdate->tm_sec = 0;

    free(sdate);
    return 0;
} // ConvertDate()


/*
 * Get day of week
 * 1 for Monday, 7 for Sunday etc.
 */
#ifdef __cplusplus
extern "C"
#endif
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


/*
 * Get day of week for date in mdy formay
 * 1 for Monday, 7 for Sunday etc.
 */
#ifdef __cplusplus
extern "C"
#endif
int DayOfWeekSt(char * adate)
{
    static int t[] = {0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4};
    int rc;
    int y, m, d;
    char * tok;
    char sdate[32];

    strcpy(sdate, adate);

    /// @todo check for errors here
    tok = strtok(sdate, "/");
    if ( tok == NULL ) return 1;
    m = atoi(tok);

    tok = strtok(NULL, "/");
    if ( tok == NULL ) return 1;
    d = atoi(tok);

    tok = strtok(NULL, "/");
    if ( tok == NULL ) return 1;
    y = atoi(tok);

    y -= m < 3;
    // value is 0 = Sunday, 1 = Monday, etc.
    rc = (y + y/4 - y/100 + y/400 + t[m-1] + d) % 7;
    if ( rc==0 ) rc = 7;

    return rc;
} // DayOfWeek()


/*
 * Replace all occurences of character in string
 */
#ifdef __cplusplus
extern "C"
#endif
void replace_char(char * in_buf,
                  char findcd,
                  char replacech,
                  char * out_buf)
{
    int i, j;

    strcpy(out_buf, in_buf);
    j = strlen(in_buf);
    for ( i=0; i<j; i++ )
    {
        if ( out_buf[i] == findcd )
        {
            out_buf[i] = replacech;
        }
    }
} // replace_char()


/*
 * Wonderful time string formats
 */
extern "C"
int time_fns_st(float itime,
             const char * ifmt,
             char * time_string)
{
    short hr_no, min_no;

    hr_no = itime / 60;
    min_no = itime - hr_no * 60;

    if ( ! strcmp(ifmt, "HHMM") )
    {
        sprintf(time_string, "%02d%02d", hr_no, min_no);
    } // if ;

    if ( ! strcmp(ifmt, "HH:MM") )
    {
        sprintf(time_string, "%02d:%02d", hr_no, min_no);
    } // if

    return 0;
} // time_fns()


/*
 * Wonderful time string formats
 */


extern "C"
char * time_fns(float itime,
                const char * ifmt)
{
    short hr_no, min_no;
    static char time_string[8]={0};

    hr_no = itime / 60;
    min_no = itime - hr_no * 60;

    if ( ! strcmp(ifmt, "HHMM") )
    {
        sprintf(time_string, "%02d%02d", hr_no, min_no);
    } // if ;

    if ( ! strcmp(ifmt, "HH:MM") )
    {
        sprintf(time_string, "%02d:%02d", hr_no, min_no);
    } // if

    return time_string;
} // time_fns()


/*
 * Wonderful time string formats
 */
extern "C"
int time_fns_int(int itime)
{
    short hr_no, min_no;

    hr_no = itime / 60;
    min_no = itime - hr_no * 60;

    return hr_no*100+min_no;
} // time_fns()
