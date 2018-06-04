/**
 * @file ssm.l

 * @brief Lexer for SSM
 *
 */

%start address sender ssm time_type msg_ref msg_type
%start flight_info
%start period_info
%start new_flight_info
%start equip_info
%start leg_info
%start segment_info
%start class_info
%start eom flush error flusherr

%{
#include <string.h>
#include "UserLogSsm.h"
#include "ssm.h"
#include "asmssm.h"
#include "readssm.tab.h"

/* to prevent spurious output */
#undef output
#define output(c)

#define unput_all() { int i; for(i = strlen(yytext) - 1; i>= 0; i--) unput(yytext[i]); }

extern int readasm;

enum yytokentype emsgtyp = NO_SEGMENT_INFO;

#define lex_userlog(lvl, format, ...) if (verbose>=lvl) printf(format "\n", ## __VA_ARGS__)

%}

MONTH (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|XXX)

DATE    (([0123][0-9]{MONTH}[0-9][0-9])|([0123][0-9]{MONTH}))

CONTROL_CHAR    (\001|\002|\003)

ACTION_IDS     (NEW|TIM|RPL|CNL|EQT|CON)

END_OF_LINE    ([\n]|[\r][\n])

%%

    /*
     * In general, the state of the lexer is called by the name
     * of the expected input line. If the line does not match
     * it goes to the error state - print the line and exit
     */

BEGIN(address);

{CONTROL_CHAR} {
    ;
}

[\.] {
    lex_userlog(3, "\nDot", NULL);
    return DOT;
}

^[A-Z]{2}[ ] {
    /* same as the above LF format */
    lex_userlog(3, "\nQuick [%s]", yytext);
    BEGIN(address);
}

[ ] {
    /* Ignore spaces */
    ;
}

    /*
     * Destination address
     */
<address>[A-Z0-9]{6,7}[\ ] {
    int n = strlen(yytext);
    yytext[n-1] = 0;
    lex_userlog(3, "\nAddress 3 [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return ADRES;
}

<address>[A-Z0-9]{6,7} {
    int n = strlen(yytext);
    yytext[n-2] = 0;
    lex_userlog(3, "\nAddress 4 [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return ADRES;
}

<address>{CONTROL_CHAR}? {
    lex_userlog(3, "\nAddress control character %s", yytext);
}

<address>. {
    lex_userlog(3, "\nAddress error [%s]", yytext);
    unput_all();
    BEGIN(error);
}

<address>{END_OF_LINE} {
    BEGIN(sender);
}

    /*
     * Sender
     */
<sender>\.[A-Z]([A-Z0-9]{6})((\ ([0-9]{6}))*) {
    /* sender. Ignore trailing garbage */
    lex_userlog(3, "\nSender [%s]", yytext);
    strcpy(yylval.sval, &yytext[1]);
    return SENDER;
}

<sender>[A-Z]([A-Z]{6})\ ([A-Z]{2}\/[0-9]{6})((\/([A-Z0-9])*)*)  {
    /* sender. Ignore trailing garbage */
    lex_userlog(3, "\nSender 2 [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return SENDER;
}

<sender>. {
    lex_userlog(3, "\nSender error [%s]", yytext);
    unput_all();
    BEGIN(error);
    /*
    BEGIN(ssm);
    */
}

<sender>{END_OF_LINE} {
    BEGIN(ssm);
}

    /*
     * File type
     */
<ssm>{CONTROL_CHAR}?SSM {
    lex_userlog(3, "\nSSM [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return MTYPE;
}

<ssm>^ASM {
    /* message type identifier */
    if ( readasm )
    {
        lex_userlog(3, "\nASM [%s]", yytext);
        strcpy(yylval.sval, yytext);
        return MTYPE;
    }
    else
    {
        lex_userlog(0, "\nASM not supported [%s]", yytext);
        unput_all();
        BEGIN(error);
    }
}

<ssm>. {
    lex_userlog(0, "\nSSM error [%s]", yytext);
    unput_all();
    BEGIN(error);
}

<ssm>{END_OF_LINE} {
    BEGIN(time_type);
}

    /*
     * Time tipe : UTC or LT
     */
<time_type>^LT  {
    /* local or UTC times - if none then UTC */
    lex_userlog(3, "\nTime [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return TTYPE;
}

<time_type>^UTC {
    lex_userlog(3, "\nTime [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return TTYPE;
}

<time_type>^{DATE} {
    lex_userlog(3, "\nDate [%s]", yytext);
    /* the ref line starts in a date */
    unput_all();
}

<time_type>. {
    lex_userlog(3, "\nTime error [%s]", yytext);
    unput_all();
    BEGIN(error);
}

<time_type>{END_OF_LINE} {
    BEGIN(msg_ref);
}

    /*
     * Message reference
     */
<msg_ref>({CONTROL_CHAR}*){ACTION_IDS}.*       {
    /* No message reference was found, move along */
    lex_userlog(3, "\nMessage ref 1 [%s]", yytext);
    unput_all();
    BEGIN(msg_type);
}

<msg_ref>.* {
    /* ref line - basically date, serial, E/C, part. No parsing */
    lex_userlog(3, "\nMessage ref junk [%s]", yytext);
}

<msg_ref>{END_OF_LINE} {
    BEGIN(msg_type);
}

    /*
     * Message type
     */
<msg_type>({CONTROL_CHAR}*)NEW.*  {
    lex_userlog(3, "\nNew [%s]", yytext);
    emsgtyp = NEW;
    return NEW;
}

<msg_type>^(([:cntrl:])?)NEW.* {
    /* new schedule SSM */
    lex_userlog(3, "\nNew 2 [%s]", yytext);
    emsgtyp = NEW;
    return NEW;
}

<msg_type>({CONTROL_CHAR}*)CNL.*        {
    lex_userlog(3, "\nCancel [%s]", yytext);
    emsgtyp = CNL;
    return CNL;
}

<msg_type>^(([:cntrl:])?)CNL.*       {
    lex_userlog(3, "\nCancel [%s]", yytext);
    emsgtyp = CNL;
    return CNL;
}

<msg_type>({CONTROL_CHAR}*)RPL.*        {
    lex_userlog(3, "\nReplace [%s]", yytext);
    emsgtyp = RPL;
    return RPL;
}

<msg_type>^(([:cntrl:])?)RPL.* {
    lex_userlog(3, "\nReplace 2 [%s]", yytext);
    emsgtyp = RPL;
    return RPL;
}

<msg_type>({CONTROL_CHAR}*)CON.*        {
    lex_userlog(3, "\nConfigure [%s]", yytext);
    BEGIN(flight_info);
    emsgtyp = CON;
    return CON;
}

<msg_type>^(([:cntrl:])?)CON.* {
    /* change of aircraft configuration SSM */
    lex_userlog(3, "\nConfigure 2 [%s]", yytext);
    emsgtyp = CON;
    return CON;
}

<msg_type>({CONTROL_CHAR}*)EQT.*        {
    lex_userlog(3, "\nEquipment [%s]", yytext);
    strcpy(yylval.sval, yytext);
    emsgtyp = EQT;
    return EQT;
}

<msg_type>^(([:cntrl:])?)EQT.* {
    /*
     * @todo change of aircraft configuration SSM to be done as CON...
     * this is for time being
    */
    lex_userlog(3, "\nEquipment 2 [%s]", yytext);
    strcpy(yylval.sval, yytext);
    emsgtyp = EQT;
    return EQT;
}

<msg_type>({CONTROL_CHAR}*)TIM.*        {
    lex_userlog(3, "\nChange time [%s]", yytext);
    emsgtyp = TIM;
    return TIM;
}

<msg_type>^(([:cntrl:])?)TIM.* {
    /* change times in schedule SSM */
    lex_userlog(3, "\nChange time [%s]", yytext);
    emsgtyp = TIM;
    return TIM;
}

<msg_type>. {
    lex_userlog(3, "\nMessage error [%s]", yytext);
    unput_all();
    BEGIN(error);
}

<msg_type>{END_OF_LINE} {
    BEGIN(flight_info);
}

    /*
     * Flight information
     */
<flight_info>^[A-Z]([A-Z]{1,2})([0-9]{1,4}) {
    lex_userlog(3, "\nFlight number 1 [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return FLIGHT;
}

<flight_info>^[A-Z]([A-Z]{1,2})([0-9]{1,4})(\ [1-9]\/[A-Z]{2,3})* {
    lex_userlog(3, "\nFlight number 2 [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return FLIGHT;
}

<flight_info>[1-9]\/[A-Z]{2,3}(\ [1-9]\/[A-Z]{2,3})*  {
    lex_userlog(3, "\nAirline [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return AIRLINE;
}

<flight_info>{END_OF_LINE} {
    BEGIN(period_info);
}

    /*
     * Flight period information
     */
<period_info>{DATE} {
    lex_userlog(3, "\nDate [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return DATEDM;
}

<period_info>[1-9]{1,7} {
    yylval.ival = atoi(yytext);
    lex_userlog(3, "\nPeriod days [%s]", yytext);
    return FREQ;
}

<period_info>{END_OF_LINE} {
    switch (emsgtyp)
    {
        case FLT :
            lex_userlog(3, "\nRead new flight", NULL);
            BEGIN(new_flight_info);
            break;
        case TIM :
            lex_userlog(3, "\nRead legs", NULL);
            BEGIN(leg_info);
            break;
        default :
            lex_userlog(3, "\nRead equipment", NULL);
            BEGIN(equip_info);
    }
}

    /*
     * New flight information
     */
<new_flight_info>^[A-Z]([A-Z]{1,2})([0-9]{1,4}) {
    lex_userlog(3, "\nNew flight number [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return FLIGHT;
}

<new_flight_info>{END_OF_LINE} {
    BEGIN(equip_info);
}

    /*
     * Equipment information
     */
<equip_info>[A-Z] {
    lex_userlog(3, "\nService type [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return STYPE;
}

<equip_info>[A-Z0-9]{3}[\ ] {
    lex_userlog(3, "\nAircraft [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return AIRCRFT;
}

<equip_info>[A-Z]{2}\. {
    /* same as the above LF format */
    lex_userlog(3, "\nPax book [%s]", yytext);
    strncpy(yylval.sval, yytext, 2);
    yylval.sval[2] = 0;
    return PAXBOOK;
}

<equip_info>[A-Z][0-9]{1,3} {
    lex_userlog(3, "\nAircraft config 2 [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return ACONFIG;
}

<equip_info>[A-Z]{2,3}[0-9]{1,5} {
    /// @todo figure out what this is
    lex_userlog(3, "\nJunk [%s]", yytext);
}

<equip_info>[A-Z]{2,3}[0-9]{1,5}[\ ] {
    /// @todo figure out what this is
    lex_userlog(3, "\nJunk2 [%s]", yytext);
}

<equip_info>[A-Z]{5} {
    lex_userlog(3, "\nTail [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return TAIL;
}

<equip_info>{END_OF_LINE} {
    switch (emsgtyp)
    {
        case EQT :
            lex_userlog(3, "\nRead segments", NULL);
            BEGIN(segment_info);
            break;
        default :
            lex_userlog(3, "\nRead legs", NULL);
            BEGIN(leg_info);
    }
}

    /*
     * Leg segment information
     */
<leg_info>[A-Z]{3}[0-9]{4} {
    lex_userlog(3, "\nLeg station [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return LEGSTN;
}

<leg_info>[\ ][1-7]{1,7} {
    lex_userlog(3, "\nLeg frequency [%s]", yytext+1);
    yylval.ival = atoi(yytext+1);
    return FREQ;
}

<leg_info>{END_OF_LINE} {
    BEGIN(segment_info);
}

<segment_info>[A-Z]{6} {
    strcpy(yylval.sval, yytext);
    lex_userlog(3, "\nSegment [%s]", yytext);
    return SEGMENT;
}

<segment_info>[\ ][0-9]{1,3} {
    yylval.ival = atoi(yytext+1);
    lex_userlog(3, "\nSegment info [%d]", yylval.ival);
    return COUNT;
}

<segment_info>\/[A-Z0-9]* {
    lex_userlog(3, "\nSegment data [%s]", yytext+1);
    strcpy(yylval.sval, yytext+1);
    return SEGDATA;
}

<segment_info>{END_OF_LINE} {
    /* @todo what comes next? */
    ;
}

    /*
     * Class information
     */
<class_info>[0-9]{1,3}\/ {
    int n;
    char cval[8];

    n = strlen(yytext);
    strncpy(cval, yytext, n);
    cval[n] = 0;
    yylval.ival = atoi(cval);
    lex_userlog(3, "\nClass code [%s]", yytext);
    return COUNT;
}

<class_info>[A-Z][A-Z0-9]* {
    lex_userlog(3, "\nClass data [%s]", yytext);
    strcpy(yylval.sval, yytext);
    return SEGMENT;
}

<class_info><<EOF>> {
    BEGIN(flush);
    return EOL;
}

<error>.* {
    lex_userlog(3, "\nError [%s]", yytext);
    return -1;
}

<flusherr>.* {
    lex_userlog(3, "\nError [%s]", yytext);
    return -1;
}

<flush>. ;

%%



