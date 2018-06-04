%{
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#include "UserLogSsm.h"
#include "readssm.tab.h"

#define yacc_userlog(format, ...) printf("\n" format, ## __VA_ARGS__)

extern int yylineno;
extern char * yytext;

extern int verbose;

int yylex();
int yyerror();

%}

%union
{
    char sval[132];
    int ival;
    double dval;
}

%type <ival> NUM2 NUM6 NUM8 NUM13 COUNT DIGIT FREQ
%type <sval> COMMID IDENTIFIER DATEDM GROUP ADRES MTYPE TTYPE STYPE FLT CSFLT FLIGHT NUM14 QK SENDER
%type <sval> EQT SEGMENT AIRCRFT PAXBOOK ACONFIG TAIL AIRLINE LEGSTN SEGDATA

%token EOL
%token NO_SEGMENT_INFO
%token DEPARTURE
%token ARRIVAL
%token DEPARTURE_ARRIVAL
%token ENTIRE_SEGMENT

%token QK
%token ADRES
%token SENDER
%token SEGMENT
%token SEGDATA
%token LEGSTN
%token AIRLINE

%token NEW
%token CNL
%token RPL
%token SKD
%token ACK
%token ADM
%token CON
%token EQT
%token FLT
%token NAC
%token REV
%token RSD
%token TIM

%token IDENTIFIER
%token COUNT
%token DIGIT
%token LETTER
%token GROUP
%token NAME
%token COMMID
%token FLIGHT
%token CSFLT
%token FREQ
%token LOCATOR
%token PAXBOOK
%token DTS
%token AMOUNT
%token TAIL
%token AIRCRFT
%token ACONFIG
%token NUM2
%token NUM6
%token NUM8
%token NUM13
%token NUM14
%token DATEDM
%token FSLASH
%token BSLASH
%token HYPHEN
%token SPACE
%token MTYPE
%token TTYPE
%token STYPE
%token DOT

/*
%nonassoc COUNT
%nonassoc NAME
*/
%start asmfile

%%

asmfile :
    | asmfile alines
    ;

alines : alines aline
    | aline
    ;

aline : addresses
    | commid
    | sender
    | mtype
    | ttype
    | action
    | period
    | flight
    | leg
    | equip
    | segment
    | classes

addresses : addresses addressel
    | addressel

addressel : ADRES
{
    userlogv(2, "*** Address element: %s", $1);
}

sender : SENDER
{
    userlogv(2, "*** Sender element: %s", $1);
}
sender : DOT SENDER
{
    userlogv(2, "*** Sender element: %s", $2);
}

mtype : MTYPE
{
    userlogv(2, "*** Message type: %s", $1);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_message_type($1);
#endif
}

ttype : TTYPE
{
    userlogv(2, "*** Time type: %s", $1);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_time_zone($1);
#endif
}

configs : configs config | config

config : ACONFIG {
    userlogv(2, "*** Config: %s", $1);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_config($1);
#endif
}

equip : STYPE AIRCRFT PAXBOOK configs
{
    userlogv(2, "*** Equipmen1: type %s aircraft %s book %s", $1, $2, $3);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_equipment($2, $3, "", "");
#endif
}

equip : STYPE AIRCRFT PAXBOOK configs TAIL
{
    userlogv(2, "*** Equipmen2: type %s aircraft %s book %s tail %s", $1, $2, $3, $5);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_equipment($2, $3, "", $5);
#endif
}

equip : STYPE AIRCRFT PAXBOOK configs SEGMENT TAIL
{
    userlogv(2, "*** Equipmen3: type %s aircraft %s book %s data %s tail %s", $1, $2, $3, $5, $6);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_equipment($2, $3, $5, $6);
#endif
}

action : new
    | cnl
    | rpl
    | skd
    | ack
    | adm
    | con
    | eqt
    | flt
    | nac
    | rev
    | rsd
    | tim

new : NEW
{
    userlogv(2, "*** New");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(NEW);
#endif
}

cnl  : CNL
{
    userlogv(2, "*** Cancel");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(CNL);
#endif
}

rpl  : RPL
{
    userlogv(2, "*** Replace");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(RPL);
#endif
}

skd  : SKD
{
    userlogv(2, "*** Skd");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(SKD);
#endif
}

ack  : ACK
{
    userlogv(2, "*** Ack");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(ACK);
#endif
}

adm  : ADM
{
    userlogv(2, "*** Adm");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(ADM);
#endif
}

con  : CON
{
    userlogv(2, "*** Configuration");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(CON);
#endif
}

eqt : EQT
{
    userlogv(2, "*** Equipment");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(EQT);
#endif
}

flt  : FLT
{
    userlogv(2, "*** Flt");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(FLT);
#endif
}

nac  : NAC
{
    userlogv(2, "*** Nac");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(NAC);
#endif
}

rev  : REV
{
    userlogv(2, "*** Rev");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(REV);
#endif
}

rsd  : RSD
{
    userlogv(2, "*** Rsd");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(RSD);
#endif
}

tim  : TIM
{
    userlogv(2, "*** Time change");
#if defined(_PROCSSM) || defined(_CHECKSSM)
    set_action(TIM);
#endif
}

period : DATEDM DATEDM FREQ
{
    userlogv(2, "*** Period: from %s to %s (days %d)", $1, $2, $3);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    if (add_dates_freq($1, $2, $3))
        return 1;
#endif
}

flight : FLIGHT AIRLINE
{
    userlogv(2, "*** Flight: number %s airline %s", $1, $2);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_flight_number($1, $2);
#endif
}

flight : FLIGHT
{
    /// @todo quick hack that throws away everything after first space
    int i;
    for (i=0; i<strlen($1); i++)
    {
        if ($1[i] == ' ')
        {
            $1[i] = 0;
            break;
        }
    }
    userlogv(2, "*** Flight: number '%s'", $1);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_flight_number($1, "");
#endif
}

leg : LEGSTN LEGSTN
{
    userlogv(2, "*** Leg: from %s to %s", $1, $2);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_leg($1, $2, 0);
#endif
}

leg : LEGSTN LEGSTN FREQ
{
    userlogv(2, "*** Leg: from %s to %s (%d)", $1, $2, $3);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_leg($1, $2, $3);
#endif
}

leg : SEGMENT SEGMENT
{
    userlogv(2, "*** Leg: from %s to %s", $1, $2);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_leg($1, $2, 0);
#endif
}

segment : SEGMENT COUNT SEGDATA
{
    char dep[8] = { 0 };
    char arr[8] = { 0 };

    strncpy(dep, $1, 3);
    strncpy(arr, &$1[3], 3);
    userlogv(2, "*** Segment 3: depart %s arrive %s code %d data %s", dep, arr, $2, $3);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_segment(dep, arr, $2, $3);
#endif
}

segment : SEGMENT COUNT SEGDATA SEGDATA
{
    char dep[8] = { 0 };
    char arr[8] = { 0 };

    strncpy(dep, $1, 3);
    strncpy(arr, &$1[3], 3);
    userlogv(2, "*** Segment 4: depart %s arrive %s code %d data %s %s", dep, arr, $2, $3, $4);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_segment(dep, arr, $2, $3);
    add_segment(dep, arr, $2, $4);
#endif
}

segment : SEGMENT COUNT SEGDATA SEGDATA SEGDATA
{
    char dep[8] = { 0 };
    char arr[8] = { 0 };

    strncpy(dep, $1, 3);
    strncpy(arr, &$1[3], 3);
    userlogv(2, "*** Segment 5: depart %s arrive %s code %d data %s %s %s", dep, arr, $2, $3, $4, $5);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_segment(dep, arr, $2, $3);
    add_segment(dep, arr, $2, $4);
    add_segment(dep, arr, $2, $5);
#endif
}

segment : SEGMENT COUNT SEGDATA SEGDATA SEGDATA SEGDATA
{
    char dep[8] = { 0 };
    char arr[8] = { 0 };

    strncpy(dep, $1, 3);
    strncpy(arr, &$1[3], 3);

    userlogv(2, "*** Segment 6: depart %s arrive %s code %d data %s %s %s %s", dep, arr, $2, $3, $4, $5, $6);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_segment(dep, arr, $2, $3);
    add_segment(dep, arr, $2, $4);
    add_segment(dep, arr, $2, $5);
    add_segment(dep, arr, $2, $6);
#endif
}

segment : SEGMENT COUNT SEGDATA SEGDATA SEGDATA SEGDATA SEGDATA
{
    char dep[8] = { 0 };
    char arr[8] = { 0 };

    strncpy(dep, $1, 3);
    strncpy(arr, &$1[3], 3);
    userlogv(2, "*** Segment 6: depart %s arrive %s code %d data %s %s %s %s %s", dep, arr, $2, $3, $4, $5, $6, $7);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_segment(dep, arr, $2, $3);
    add_segment(dep, arr, $2, $4);
    add_segment(dep, arr, $2, $5);
    add_segment(dep, arr, $2, $6);
    add_segment(dep, arr, $2, $7);
#endif
}

classes : STYPE SEGMENT
{
    userlogv(2, "*** Class: type %s data %s", $1, $2);
}

classes : STYPE COUNT SEGMENT
{
    char dep[8] = { 0 };
    char arr[8] = { 0 };

    strncpy(dep, $1, 3);
    strncpy(arr, &$1[3], 3);
    userlogv(2, "*** Class: type %s code %d data %s", $1, $2, $3);
#if defined(_PROCSSM) || defined(_CHECKSSM)
    add_segment(dep, arr, $2, $3);
#endif
}

classes : SEGMENT
{
    int n = strlen($1);
    /* Ignore blanks */
    if (n > 0 && isprint($1[0])) {
        userlogv(2, "*** Class: data '%s' %d bytes", $1, n);
#if defined(_PROCSSM) || defined(_CHECKSSM)
        add_segment("", "", 0, $1);
#endif
    }
}

commid : DOT COMMID NUM6
{
    userlogv(2, "*** Communication: %s %06d", $2, $3);
}

%%

int yyerror(char *s)
{
    fprintf(stderr, "Yacc error: %s at line %d '%s'", s, yylineno,  yytext);
}
