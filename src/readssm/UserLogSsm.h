/**
 * @file UserLogSsm.h
 *
 * Write log messages
 */
#ifndef SSM_USERLOG_H
#define SSM_USERLOG_H

#include <stdio.h>

extern int verbose;
extern FILE * ssmlog;

#define userlog(format, ...) {fprintf(ssmlog,"\n%s[%s +%d]\t",__FUNCTION__,__FILE__,__LINE__);fprintf(ssmlog,format, ## __VA_ARGS__);fflush(ssmlog);}
#define userlogv(lvl, format, ...) if (verbose>=lvl){fprintf(ssmlog,"\n%s[%s +%d]\t",__FUNCTION__,__FILE__,__LINE__);fprintf(ssmlog,format, ## __VA_ARGS__);fflush(ssmlog);}

#define SHOW_DB_ERROR(format,...) fprintf(ssmlog,"PostgreSQL error %s :",SQLSTATE);fprintf(ssmlog,format, ## __VA_ARGS__);fflush(ssmlog);

#define CHECK_DB_RESULT(format, ...) \
if(sqlca.sqlcode){fprintf(ssmlog,"\n%s[%s +%d]\t",__FUNCTION__,__FILE__,__LINE__);fprintf(ssmlog,"PostgreSQL error %s :",SQLSTATE);fprintf(ssmlog,format, ## __VA_ARGS__);fflush(ssmlog);return -1;}\
else if (verbose>=3){fprintf(ssmlog,"\n%s[%s +%d]\t",__FUNCTION__,__FILE__,__LINE__);fprintf(ssmlog,format, ## __VA_ARGS__);fflush(ssmlog);}

#define LOG_DB_RESULT(format, ...) \
{fprintf(ssmlog,"\n%s[%s +%d]\t",__FUNCTION__,__FILE__,__LINE__);fprintf(ssmlog,"PostgreSQL state %s (code %ld) :",SQLSTATE, SQLCODE);fprintf(ssmlog,format, ## __VA_ARGS__);fflush(ssmlog);}

#endif
