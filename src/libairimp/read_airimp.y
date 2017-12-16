%{
#include <stdio.h>
#include <string.h>

#define YYLMAX 10240

// int yydebug=0;
//
int verbose;
int airimperr;

extern FILE * yyin;
extern int yylineno;
int yyerrstatus;
extern char * yytext;
%}

%union
{
    char sval[1024];
    int ival;
    double dval;
}

%token ADDR
%token QK
%token QU
%token SA
%token YY

%token ASC
%token AVS
%token DVD
%token NAC
%token NCO
%token NAR
%token NRL
%token PDM
%token TRL

%token ARNK
%token RECLOC
%token TITLE
%token IDENTIFIER
%token CHNT
%token DOT
%token DASH
%token NAME
%token COMMID
%token FLIGHT
%token CSFLT
%token FLT
%token DTS
%token AMOUNT
%token NUMBER
%token ALNUM
%token DATEDM
%token DATEDMY
%token FSLASH
%token BSLASH
%token ACTION
%token SSRCODE
%token TKNE
%token TKDG
%token CKIN
%token PAXNUM
%token PAXNAME
%token PAXCOUNT
%token AIRPORT

%token OSI
%token DOB
%token CTCA
%token CTCB
%token CTCE
%token CTCF
%token CTCH
%token CTCM
%token CTCT
%token CTCP
%token NXTM

%token TEXT

%token SSR
%token AILO
%token AILR
%token BIKE
%token CCNM
%token CHLN
%token CLID
%token DOCA
%token DOCO
%token DOCS
%token ECAR
%token EDCO
%token FARE
%token FARX
%token FOID
%token FQTV
%token FLOT
%token GRPF
%token GRPS
%token INFT
%token LANG
%token RRTX
%token CHLD
%token FCD
%token NSSA
%token OTHS
%token PAXT
%token PCCC
%token RRTP
%token RRCA
%token RRCB
%token RRCE
%token RRCP
%token EMAIL
%token SEAT
%token SPEQ
%token TKNM
%token VOYG
%token XBAG
%token NSST
%token AIRLINE
%token EOL

%type <sval> RECLOC TEXT EMAIL ADDR FLIGHT DATEDM DATEDMY PAXNAME TITLE IDENTIFIER CSFLT ACTION AIRPORT SSRCODE ALNUM COMMID AIRLINE
%type <dval> AMOUNT
%type <ival> PAXNUM PAXCOUNT NUMBER

%start airimps

%%

airimps : airimps airimp
    | airimp
    | blanks
    | error '\n'
{
    yyerrok;
}

airimp : address commid reclocs paxes flights alines blanks
    | address commid reclocs paxes flights blanks
    | address commid reclocs flights alines blanks
    | address commid reclocs paxes alines blanks
    | address commid actions reclocs paxes flights alines blanks
    | address commid actions reclocs paxes flights blanks
    | address commid reclocs actions flights alines blanks
    | address commid actions flights blanks
    | address commid reclocs alines blanks
    | address commid alines
    ;

blanks : blanks blank
    | blank
    | /* nothing */
    ;

blank : EOL
    ;

actions : actions action
    | action
    ;

action : dvd
    | avs
    | asc
    | nac
    | nar
    | nco
    | nrl
    | pdm
    | trl
    ;

reclocs : reclocs recloc
    | recloc
    ;

recloc : RECLOC EOL
{
    if (verbose) printf("recloc");
    printf("*** Record locator\n");
}

recloc : RECLOC TEXT EOL
{
    if (verbose) printf("recloc");
    printf("*** Record locator %s ref '%s'\n", $1, $2);
}

recloc : RECLOC NUMBER EOL
{
    if (verbose) printf("recloc");
    printf("*** Record locator %s ref %d\n", $1, $2);
}

recloc : RECLOC FLIGHT EOL
{
    if (verbose) printf("recloc");
    printf("*** Record locator %s ref '%s'\n", $1, $2);
}

recloc : RECLOC AIRPORT EOL
{
    if (verbose) printf("recloc");
    printf("*** Record locator %s ref '%s'\n", $1, $2);
}

flights : flights flight
    | flight
    ;

alines : alines aline
    | aline
    | blank
    ;

aline : osi
    | ssr
    | dob
    | ctca
    | ctcb
    | ctce
    | ctcf
    | ctch
    | ctcm
    | ctcp
    | ctct
    | nxtm
    /*
    */
    | ailo
    | ailr
    | bike
    | ccnm
    | docs
    | chld
    | chln
    | ckin
    | clid
    | doca
    | doco
    | ecar
    | edco
    | fare
    | farx
    | grpf
    | grps
    | foid
    | fqtv
    | flot
    | inft
    | lang
    | nssa
    | nsst
    | oths
    | paxt
    | pccc
    | rrca
    | rrcb
    | rrce
    | rrcp
    | rrtp
    | rrtx
    | seat
    | speq
    | tkdg
    | tkne
    | tknm
    | voyg
    | xbag
    ;

address : ADDR EOL
{
    if (verbose) printf("address");
    printf("\n*** Address '%s'\n", $1);
    set_address($1);
}

address : QU ADDR EOL
{
    if (verbose) printf("address");
    printf("\n*** Address '%s'\n", $2);
    set_address($2);
}

address : QK ADDR EOL
{
    if (verbose) printf("address");
    printf("\n*** Address '%s'\n", $2);
    set_address($2);
}

commid : COMMID ALNUM EOL
{
    if (verbose) printf("commid");
    printf("*** Communication identifier origin %s ref %s\n", $1, $2);
    set_commid($1, $2);
}

 /*
commid : COMMID NUMBER NAME EOL
{
    printf("*** Communication identifier %d '%s'\n", $2, $3);
}
 */

paxes : paxes pax
    | paxes chnt paxes chnt paxes
    | paxes chnt paxes
    | pax
    ;

pax : PAXCOUNT PAXNAME EOL
{
    if (verbose) printf("pax");
    printf("*** Passenger %d '%s'\n", $1, $2);
}

pax : PAXCOUNT PAXNAME
{
    if (verbose) printf("pax");
    printf("*** Passenger %d '%s'\n", $1, $2);
}

pax : PAXNAME EOL
{
    if (verbose) printf("pax");
    printf("*** Passenger '%s'\n", $1);
}

pax : PAXNAME
{
    if (verbose) printf("pax");
    printf("*** Passenger '%s'\n", $1);
}

    /*
pax : paxnt chnt paxnt
    | paxn chnt pax
    | paxnt
    | paxn
    ;

paxn : PAXNUM PAXNAME EOL
{
    printf("*** Passenger %d '%s'\n", $1, $2);
}

paxn : PAXNUM PAXNAME
{
    printf("*** Passenger %d '%s'\n", $1, $2);
}

paxnt : PAXNUM PAXNAME TITLE EOL
{
    printf("*** Passenger %d '%s %s'\n", $1, $2, $3);
}
    */

flight : FLIGHT DATEDMY AIRPORT ACTION EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s airports %s action %s\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4);
}

flight : FLIGHT DATEDM AIRPORT ACTION EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s airports %s action '%s'\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4);
}

flight : FLIGHT DATEDM ACTION AIRPORT
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s action '%s' airports %s\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4);
}
flight : FLIGHT DATEDM ACTION AIRPORT EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s action '%s' airports %s\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4);
}

flight : FLIGHT DATEDMY AIRPORT ACTION TEXT EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s airports %s action '%s%s'\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4, $5);
}

flight : FLIGHT DATEDM AIRPORT ACTION TEXT EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s airports %s action '%s%s'\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4, $5);
}

flight : CSFLT DATEDMY AIRPORT ACTION EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Codeshare flight %s class %c date %c%c %s airports %s action '%s'\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4);
}

flight : CSFLT DATEDM AIRPORT ACTION EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Codeshare flight %s class %c date %c%c %s airports %s action '%s'\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4);
}

flight : CSFLT DATEDMY AIRPORT ACTION TEXT EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Codeshare flight %s class %c date %c%c %s airports %s action '%s%s'\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4, $5);
}

flight : CSFLT DATEDM AIRPORT ACTION TEXT EOL
{
    int n = strlen($1);
    char fclass = $1[n-1];
    $1[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Codeshare flight %s class %c date %c%c %s airports %s action '%s%s'\n", $1, fclass, $2[0], $2[1], &$2[2], $3, $4, $5);
}

flight : ARNK EOL
{
    if (verbose) printf("flight");
    printf("*** Arrival unknown\n");
}

asc : ASC EOL
{
    if (verbose) printf("asc");
    printf("*** Advice of schedule change\n");
}

avs : AVS EOL
{
    if (verbose) printf("avs");
    printf("*** Availability status\n");
}

chnt : CHNT TEXT EOL
{
    if (verbose) printf("chnt");
    printf("*** Change to name '%s'\n", $2);
}

chnt : CHNT EOL
{
    if (verbose) printf("chnt");
    printf("*** Change to name\n");
}

dvd : DVD EOL
{
    if (verbose) printf("dvd");
    printf("*** Divided PNR\n");
}

nar : NAR EOL
{
    if (verbose) printf("nar");
    printf("*** New arrival\n");
}

nac : NAC EOL
{
    if (verbose) printf("nac");
    printf("*** No action taken\n");
}

nrl : NRL EOL
{
    if (verbose) printf("nrl");
    printf("*** Non return leg\n");
}

nco : NCO EOL
{
    if (verbose) printf("nco");
    printf("*** New continuation\n");
}

pdm : PDM EOL
{
    if (verbose) printf("pdm");
    printf("*** Possible duplicate\n");
}

osi : OSI AIRPORT EOL
{
    if (verbose) printf("osi");
    printf("*** Other service information '%s'\n", $2);
}

osi : OSI TEXT EOL
{
    if (verbose) printf("osi");
    printf("*** Other service information '%s'\n", $2);
}

trl : TRL EOL
{
    if (verbose) printf("trl");
    printf("*** Migrated PNR\n");
}

dob : OSI DOB TEXT EOL
{
    if (verbose) printf("dob");
    printf("*** Date of birth '%s'\n", $3);
}

ctca : OSI CTCA TEXT EOL
{
    if (verbose) printf("ctca");
    printf("*** Contact information '%s'\n", $3);
}

ctcb : OSI CTCB TEXT EOL
{
    if (verbose) printf("ctcb");
    printf("*** Contact information '%s'\n", $3);
}

/* TODO Figure out the junk rule */
ctce : OSI CTCE TEXT EOL
     | OSI CTCE EMAIL EOL
{
    if (verbose) printf("ctce");
    printf("*** Contact email '%s'\n", $3);
}

ctcf : OSI CTCF TEXT EOL
{
    if (verbose) printf("ctcf");
    printf("*** Contact information '%s'\n", $3);
}

ctch :  OSI CTCH TEXT EOL
{
    if (verbose) printf("ctch");
    printf("*** Contact information '%s'\n", $3);
}

ctcm : OSI CTCM TEXT EOL
{
    if (verbose) printf("ctcm");
    printf("*** Contact information '%s'\n", $3);
}

ctcp : OSI CTCP TEXT EOL
{
    if (verbose) printf("ctcp");
    printf("*** Contact information '%s'\n", $3);
}

ctct : OSI CTCT TEXT EOL
{
    if (verbose) printf("ctct");
    printf("*** Contact information '%s'\n", $3);
}

nxtm :  OSI NXTM TEXT EOL
{
    if (verbose) printf("nxtm");
    printf("*** Contact information '%s'\n", $3);
}

/** SPECIAL SERVICE REQUESTS **/


ailo :  SSR AILO AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME EOL
{
    printf("*** Insurance '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9);
}

ailr :  SSR AILR AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME EOL
{
    printf("*** Insurance '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9);
}

bike : SSR BIKE AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME COMMID EOL
{
    printf("*** Bicycle '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $10);
}

bike : SSR BIKE AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Bicycle '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

ccnm : SSR CCNM TEXT EOL
{
    printf("*** Credit card number '%s'\n", $3);
}

chld : SSR CHLD AIRLINE ACTION PAXCOUNT PAXNAME EOL
{
    printf("*** Child airline '%s' action '%s' passenger %d '%s'\n", $3, $4, $5, $6);
}

chld : SSR CHLD AIRLINE ACTION PAXCOUNT PAXNAME DOT DATEDMY EOL
{
    printf("*** Child airline '%s' action '%s' passenger %d '%s' date '%s'\n", $3, $4, $5, $6, $8);
}

chld : SSR CHLD AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Child airline '%s' action '%s' passenger %d '%s' date '%s'\n", $3, $4, $5, $6, $8);
}

chld : SSR CHLD AIRLINE ACTION PAXCOUNT PAXNAME DOT EOL
{
    printf("*** Child airline '%s' action '%s' passenger %d '%s'\n", $3, $4, $5, $6);
}

chln : SSR CHLN AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Checkin stuff '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT DATEDM EOL
{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT DATEDMY EOL
{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT DATEDMY EOL
{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME EOL
{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9);
}

ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDM DOT DATEDMY EOL
{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $9);
}

ckin : SSR CKIN AIRLINE ACTION PAXCOUNT PAXNAME DOT DATEDMY EOL
{
    printf("*** Checkin airline '%s' action '%s' passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $8);
}

clid : SSR CLID AIRLINE TEXT EOL
{
    printf("*** Caller ID airline %s value '%s'\n", $3, $4);
}

doca : SSR DOCA AIRLINE ACTION TEXT EOL
{
    printf("*** Fubar docs '%s' action '%s' value '%s'\n", $3, $4, $5);
}

doco : SSR DOCO AIRLINE ACTION TEXT EOL
{
    printf("*** Documents airline '%s' action '%s' value '%s'\n", $3, $4, $5);
}
docs : SSR DOCS AIRLINE FSLASH TEXT EOL
{
    printf("*** Documents airline '%s' value '%s'\n", $3, $5);
}
docs : SSR DOCS AIRLINE ACTION TEXT EOL
{
    printf("*** Documents airline '%s' action '%s' value '%s'\n", $3, $4, $5);
}

ecar : SSR ECAR AIRLINE ACTION AIRPORT TEXT EOL
{
    printf("*** Car hire '%s'\n", $3);
}

edco : SSR EDCO AIRLINE ACTION AIRPORT TEXT EOL
{
    printf("*** Edcon '%s'\n", $3);
}

foid : SSR FOID AIRLINE ACTION TEXT EOL
{
    printf("*** Fubar '%s' action '%s' value '%s'\n", $3, $4, $5);
}

grpf : SSR GRPF AIRLINE TEXT EOL
{
    printf("*** Other airline '%s' text '%s'\n", $3, $4);
}

grps : SSR GRPS AIRLINE TEXT EOL
{
    printf("*** Other airline '%s' text '%s'\n", $3, $4);
}

inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Infant name '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT DATEDMY EOL
{
    printf("*** Infant name '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT DATEDMY EOL
{
    printf("*** Infant name '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL
{
    printf("*** Infant name '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $9);
}

/*
inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Infant airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}
*/

fare : SSR FARE AIRLINE TEXT EOL
{
    printf("*** Fare airline %s value '%s'\n", $3, $4);
}

farx : SSR FARX AIRLINE TEXT EOL
{
    printf("*** Fare airline %s extra '%s'\n", $3, $4);
}

fqtv : SSR FQTV AIRLINE TEXT EOL
{
    printf("*** Frequent traveller airline %s value '%s'\n", $3, $4);
}

flot : SSR FLOT AIRLINE ACTION AIRPORT TEXT EOL
{
    printf("*** Flight other '%s'\n", $3);;
}

lang : SSR LANG AIRLINE ACTION AIRPORT TEXT EOL
{
    printf("*** Language '%s'\n", $3);
}

lang : SSR LANG AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL
{
    printf("*** Language airline '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $9);
}

nssa : SSR NSSA AIRLINE ACTION AIRPORT NUMBER DATEDM EOL
{
    printf("*** Nasty stuff airline '%s' action '%s' airports '%s' number %04d class %c date %s\n",
           $3, $4, $5, $6, $7[0], &$7[1]);
}

nsst : SSR NSST AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL
{
    printf("*** Nasty stuff airline '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $9);
}

oths : SSR OTHS AIRLINE TEXT EOL
{
    printf("*** Other airline '%s' text '%s'\n", $3, $4);
}

paxt : SSR PAXT AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Child airline '%s' action '%s' passenger %d '%s' value '%s'\n", $3, $4, $5, $6, $8);
}

/*pccc : SSR PCCC AIRLINE ACTION AIRPORT TEXT EOL
{
    printf("*** Passenger check '%s'\n", $3);
}*/
pccc : SSR PCCC AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Passenger check airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

rrca : SSR RRCA AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** RRT airline %s action %s passenger %d '%s' phone '%s'\n", $3, $4, $5, $6, $8);
}

/*     1   2    3       4      5        6       7   8    9 */
rrcb : SSR RRCB AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** RRT airline %s action %s passenger %d '%s' date of birth '%s'\n", $3, $4, $5, $6, $8);
}

rrce : SSR RRCE AIRLINE ACTION PAXCOUNT PAXNAME EMAIL EOL
{
    printf("*** RRT airline %s action %s pax %d '%s' email '%s'\n", $3, $4, $5, $6, $7);
}

rrcp : SSR RRCP AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** RRT airline %s action %s passenger %d '%s' phone '%s'\n", $3, $4, $5, $6, $8);
}

rrtp : SSR RRTP AIRLINE ACTION TEXT EOL
{
    printf("*** RRT airline %s action '%s' price '%s'\n", $3, $4, $5);
}

rrtx : SSR RRTX AIRLINE ACTION TEXT EOL
{
    printf("*** RRT airline %s action %s extra '%s'\n", $3, $4, $5);
}

/*     1   2    3       4      5       6      7      8   9    10 */
seat : SSR SEAT AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL
{
    printf("*** Seat airline '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $9);
}

/*     1   2    3       4      5       6      7      8        9       10  11   12 */
seat : SSR SEAT AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Seat airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

/*     1   2    3       4      5       6      7       8        9       10  11   12 */
seat : SSR SEAT AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Seat airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

speq : SSR SPEQ AIRLINE ACTION AIRPORT NUMBER DATEDM TEXT EOL
{
    printf("*** Sport airline '%s' action '%s'' airports '%s' number %04d class %c date %s equipment '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $8);
}

/*     1   2    3       4      5       6      7       8        9       10  11   12 */
speq : SSR SPEQ AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Sport airline '%s' action '%s'' airports '%s' number %04d class %c date %s passenger %d '%s' equipment '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

tkne : SSR TKNE AIRLINE FSLASH TEXT EOL
{
    printf("*** E-Ticket number1 airline '%s' value '%s'\n", $3, $5);
}

/*     1   2    3       4      5       6      7      8        9   10  */
tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME EOL
{
    printf("*** E-Ticket number2 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9);
}

tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL
{
    printf("*** E-Ticket number3 airline '%s' action '%s' airports '%s' number %04d class %c date %s number '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $9);
}

/*     1   2    3       4      5       6      7      8        9       10  11     12 */
tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT NUMBER EOL
{
    printf("*** E-Ticket number4 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value %d\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}
/*     1   2    3       4      5       6      7       8        9       10  11     12 */
tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT NUMBER EOL
{
    printf("*** E-Ticket number5 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value %d\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}
tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** E-Ticket number6 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

/*     1   2    3       4      5       6      7       8        9       10  11     12 */
tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** E-Ticket number7 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

tkdg : SSR TKDG AIRLINE ACTION AIRPORT NUMBER DATEDM TEXT EOL
{
    printf("*** Ticket airline '%s' action '%s' airports '%s' class %c date %s number '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $8);
}

tknm : SSR TKNM TEXT EOL
{
    printf("*** Ticket number '%s'\n", $3);
}

tknm : SSR TKNM AIRLINE AIRLINE TEXT EOL
{
    printf("*** Ticket airline '%s' number '%s%s'\n", $3, $4, $5);
}

voyg : SSR VOYG AIRLINE TEXT EOL
{
    printf("*** Voyager miles airline '%s' value '%s'\n", $3, $4);
}

/*     1   2    3       4      5       6      7      8        9       10  11  */
xbag : SSR XBAG AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Excess baggage airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

/*     1   2    3       4      5       6      7       8        9       10  11  */
xbag : SSR XBAG AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL
{
    printf("*** Excess baggage airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n", $3, $4, $5, $6, $7[0], &$7[1], $8, $9, $11);
}

/*
ssr : SSR SSRCODE TEXT EOL
{
    if (verbose) printf("ssr");
    printf("*** Request %s '%s'\n", $2, $3);
}
*/

ssr : SSR TEXT EOL
{
    if (verbose) printf("ssr");
    printf("*** Junk SSR '%s'\n", $2);
}

 /*
junk : NAME FSLASH CSFLT NUMBER EOL
{
    printf("*** Junk '%s' '%s' %d\n", $1, $3, $4);
}
 */

%%


yyerror(char *s)
{
    fprintf(stderr, "\nError: %s at line %d '%s'\n", s, yylineno,  yytext);
    ++airimperr;
}



