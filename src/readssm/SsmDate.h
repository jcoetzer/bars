/**
 * @file SsmDate.h
 *
 * Read date in any format and convert
 */
#ifndef SSMDATE_H
#define SSMDATE_H

/**
 * Write timestamp to log
 *
 * @param msg   message
 */
void TimeStamp(const char * msg);

/**
 * Write timestamp to log
 *
 * @param msg   message
 */
void DateTimeStamp(const char * msg);

/**
 * Date time in format yyyymmddThhmmss for use in log file name
 *
 * @return timestamp
 */
char * GetDateTimeStamp();

#endif // SSMDATE_H
