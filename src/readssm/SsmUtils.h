/**
 * @file SsmUtils.h
 *
 * Support functions
 */
#ifndef SSM_UTILS_H
#define SSM_UTILS_H

#include <time.h>

// #include "FlightData.h"

#define    time2short(T)    (((T) / 100) * 60 + ((T) % 100))
#define    dci(D, A)        ((A) - (D))

/**
 * Trim trailing spaces
 *
 * Strip any trailing whitespace from a string. The definition of whitespace is the same
 * as that of the standard C library call isspace()
 *
 * @param string    input
 *
 * @return output string
 */
#ifdef __cplusplus
extern "C"
#endif
char * strrtrim(char * string);

/*
 * Create timestamp
 *
 * @param create_dts    buffer
 */
char * crea_date_time(char* create_dts);

/*
 * Create timestamp
 *
 * @return    text buffer
 */
#ifdef __cplusplus
extern "C"
#endif
char * crea_date_time_iso();

/**
 * Convert string to date
 *
 * @param dt    date string
 *
 * @return date value
 */
const long str2date(const char *dt);

/**
 * Add the date difference
 *
 * @param flightDate            flight date
 * @param flDate                flight date
 * @param origFlDate            original flight date
 *
 * @return zero upon success otherwise non-zero
 */
int addDateDifferenceL(long *flightDate,
                      const long flDate,
                      const long origFlDate);

/**
 * Add the date difference
 *
 * @param flightDate            flight date as a number
 * @param flDate                flight date as a string
 * @param flDateLen             flight date buffer size
 * @param origFlDate            original flight date
 *
 * @return zero upon success otherwise non-zero
 */
int addDateDifference(long *flightDate,
                      const char * flDate,
                      size_t flDateLen,
                      const char *origFlDate);

/**
 * Get database error message
 *
 * @param finderrNo error number
 * @param[out] text error message text
 *
 * @return zero upon success otherwise non-zero
 */
int getDBErrorStringFromNumber(int finderrNo,
                               char *text);


/**
 * Convert string to frequency codes
 *
 * @param days frequency string
 * @param datechg date change indicator
 *
 * @return some kind of buffer
 */
#ifdef __cplusplus
extern "C"
#endif
char * str2freq(char *days,
                int datechg);


/**
 * Check if frequency is a subset
 *
 * @todo figure out what this turkey does
 *
 * @param newFrequency  new frequency code
 * @param oldFrequency  old frequency to change
 * @param[out] subset  subset indicator
 *
 * @return zero upon success otherwise non-zero
 */
#ifdef __cplusplus
extern "C"
#endif
int isSubset(char *newFrequency,
             char *oldFrequency,
             int *subset);

/**
 * Set up new frequencies
 *
 * @param newFrequency             new frequency code
 * @param oldFrequencyToChange     old frequency to change
 * @param oldFrequencyToChangeSize length of old frequency to changed
 * @return zero upon success otherwise non-zero
 */
#ifdef __cplusplus
extern "C"
#endif
int differentiateFrequencies(char *newFrequency,
                             char *oldFrequencyToChange,
                             int oldFrequencyToChangeSize);

/**
 * Get some sort of intersection
 *
 * @param pFlightDataPtr data stuffies
 * @return zero upon success otherwise non-zero
 */
#ifdef __cplusplus
extern "C"
#endif
int getSetIntersect(struct FlightData * pFlightDataPtr);

/**
 * Get frequencies for split flight
 *
 * @param pFlightDataPtr    flight data
 * @param setIntersect      intersection of flight periods
 *
 * @return zero upon success otherwise non-zero
 */
#ifdef __cplusplus
extern "C"
#endif
int getFrequenciesForSplit(struct FlightData * pFlightDataPtr,
                           int *setIntersect);

/**
 * Alter frequency code
 *
 * @param frequency         frequency code
 * @param frequencySize     maximum length
 *
 * @return zero upon success otherwise non-zero
 */
#ifdef __cplusplus
extern "C"
#endif
int alterFrequency(char *frequency,
                   size_t frequencySize);

/**
 * Copy src to string dst of size siz.
 *
 * At most siz-1 characters will be copied.  Always NUL terminates (unless siz == 0).
 *
 * @param dst destination string
 * @param src source string
 * @param siz maximum number of characters to copy
 *
 * @return strlen(src); if retval >= siz, truncation occurred.
 */
#ifdef __cplusplus
extern "C"
#endif
size_t strlcpy(char * __restrict dst,
               const char * __restrict src,
               size_t siz);

/**
 * Append to string
 *
 * Appends src to string dst of size siz (unlike strncat, siz is the
 * full size of dst, not space left).  At most siz-1 characters
 * will be copied.  Always NUL terminates (unless siz <= strlen(dst)).
 * Returns strlen(src) + MIN(siz, strlen(initial dst)).
 * If retval >= siz, truncation occurred.
 *
 * @param dst destination string
 * @param src source string
 * @param siz maximum number of characters to copy
 * @return strlen(src); if retval >= siz, truncation occurred.
 */
size_t strlcat(char *dst,
               const char *src,
               size_t siz);

/**
 * Combine frequency codes
 *
 * @param frequencyCumulator    accumulated frequencies
 * @param queryFrequencyCode    frequency code to be checked
 *
 * @return zero or something
 */
#ifdef __cplusplus
extern "C"
#endif
int combineFrequencies(char *frequencyCumulator,
                       char *queryFrequencyCode);

/**
 * Return useful stuff
 *
 * @todo does this even work??
 *
 * @param s     useful buffer
 *
 * @return useful stuff
 */
#ifdef __cplusplus
extern "C"
#endif
char *dashOut(char *s);


/**
 * Create old inventory segment table
 *
 * @param flightNumber               flight number
 * @param[out] tableCreated          create indicator
 *
 * @return zero upon success otherwise non-zero
int createOldInventrySegmentTable(char *flightNumber,
                                  int *tableCreated);
 */

/**
 * Add days to date
 *
 * @param date      unix date structure
 * @param days      number of days
 *
 * @return zero upon success otherwise non-zero
 */
void DatePlusDays(struct tm* date,
                  int days);

/**
 * Get day of week
 *
 * @param y     year
 * @param m     month
 * @param d     day
 *
 * @return 1 for Monday, 7 for Sunday etc.
 */
#ifdef __cplusplus
extern "C"
#endif
int DayOfWeek(int y,
              int m,
              int d);

/**
 * Get day of week
 *
 * @param adate date in format MM/DD/YYYY
 *
 * @return 1 for Monday, 7 for Sunday etc.
 */
#ifdef __cplusplus
extern "C"
#endif
int DayOfWeekSt(char * adate);

/**
 * Replace all occurences of character in string
 *
 * @param in_buf        input buffer
 * @param findcd        character to search for
 * @param replacech     character to replace it with
 * @param out_buf       output buffer
 */
#ifdef __cplusplus
extern "C"
#endif
void replace_char(char * in_buf,
                  char findcd,
                  char replacech,
                  char * out_buf);

/**
 * Call this procedure for time string formats
 *
 * @param itime     internal time
 *
 * @return zero upon success otherwise non-zero
 */
int time_fn(int itime);

/**
 * Call this procedure for time string formats
 *
 * @param itime     internal time
 * @param ifmt          format
 */
#ifdef __cplusplus
extern "C"
#endif
char * time_fns(float itime,
                const char * ifmt);

/**
 * Call this procedure for time string formats
 *
 * @param itime         internal time
 * @param ifmt          format
 * @param time_string   buffer
 *
 * @return zero upon success otherwise non-zero
 */
#ifdef __cplusplus
extern "C"
#endif
int time_fns_st(float itime,
                const char * ifmt,
                char * time_string);

/**
 * Call this procedure for time string formats
 *
 * @param itime     internal time
 *
 * @return zero upon success otherwise non-zero
 */
#ifdef __cplusplus
extern "C"
#endif
int time_fns_int(int itime);


#endif /* SSM_UTILS_H */

