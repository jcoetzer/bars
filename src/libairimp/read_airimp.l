
/*
%option debug
*/
%option yylineno

%start stateAIRIMP
%start stateCOMMID
%start stateOSI
%start stateSSR
%start statePAX
%start stateTEXT
%start statePAXNAME
%start stateRRFARE
%start stateFLIGHT
%start stateRRJUNK
%start stateRRSTUF
%start stateMERDE

/* tokens */
%{
#include "read_airimp.tab.h"

extern int verbose;
%}

%%

[ ][\.]     {
    if (verbose>=2) printf(" dot");
    return DOT;
}
^[\.]        {
    if (verbose>=2) printf(" dot");
    return DOT;
}
[-]        {
    if (verbose>=2) printf(" dash");
    return DASH;
}
[\n<\\]     {
    if (verbose>=2) printf("\n");
    BEGIN stateAIRIMP;
    return EOL;
}
[\/]        {
    if (verbose>=2) printf(" fslash");
    return FSLASH;
}
[ ]+        ;
(MR|MRS|MISS|MS|DR|PROF) {
    if (verbose>=2) printf(" title[%s]", yytext);
    return TITLE;
}
JNB7[RU]SA  {
    if (verbose>=2) printf(" addr");
    strcpy(yylval.sval, yytext);
    return ADDR;
}
(MUCCSSA|MUCQSSA)  {
    if (verbose>=2) printf(" addr");
    strcpy(yylval.sval, yytext);
    return ADDR;
}
MUCRISA {
    if (verbose>=2) printf(" addr");
    strcpy(yylval.sval, yytext);
    return ADDR;
}
(SWIRI1G|SWIRM1G) {
    if (verbose>=2) printf(" addr");
    strcpy(yylval.sval, yytext);
    return ADDR;
}
[ ]JNB7[RU]SA  {
    if (verbose>=2) printf(" addr");
    strcpy(yylval.sval, &yytext[1]);
    return ADDR;
}
[ ](MUCCSSA|MUCQSSA)  {
    if (verbose>=2) printf(" addr");
    strcpy(yylval.sval, &yytext[1]);
    return ADDR;
}
[ ]MUCRISA {
    if (verbose>=2) printf(" addr");
    strcpy(yylval.sval, &yytext[1]);
    return ADDR;
}
[ ](SWIRI1G|SWIRM1G) {
    if (verbose>=2) printf(" addr");
    strcpy(yylval.sval, &yytext[1]);
    return ADDR;
}
QK          {
    if (verbose>=2) printf(" qk");
    return QK;
}
QU          {
    if (verbose>=2) printf(" qu");
    return QU;
}
ARNK         {
    if (verbose>=2) printf(" arnk");
    return ARNK;
}
ASC         {
    if (verbose>=2) printf(" asc");
    return ASC;
}
AVS         {
    if (verbose>=2) printf(" avs");
    return AVS;
}
DVD         {
    if (verbose>=2) printf(" dvd");
    return DVD;
}
NCO         {
    if (verbose>=2) printf(" nco");
    return NCO;
}
NAC         {
    if (verbose>=2) printf(" nac");
    return NAC;
}
NAR         {
    if (verbose>=2) printf(" nar");
    return NAR;
}
PDM         {
    if (verbose>=2) printf(" pdm");
    return PDM;
}
TRL         {
    if (verbose>=2) printf(" trl");
    return TRL;
}
(MUCSA|HDQJE|SWI1G|JNBSA|JNBJE|MUC1A)[ ] {
    if (verbose>=2) printf(" recloc[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateTEXT;
    return RECLOC;
}
<stateAIRIMP>(HK|KK|SS|XX|CS|CH|HN|UN|TK|CX|CN|UC|NN|HL|PU|LC|LA|HX|NO|RR)[0-9]{1,2}     {
    if (verbose>=2) printf(" action[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateTEXT;
    return ACTION;
}
 /* BFN|CPT|DUR|GRJ|HLA|JNB|PLZ|ZNZ { */
 /*    printf( "AIRPORT [%s]", yytext);*/
 /*    strcpy(yylval.sval, yytext);*/
 /*    return AIRPORT;*/
 /* } */
SSR         {
    if (verbose>=2) printf(" ssr");
    BEGIN stateSSR;
    return SSR;
}
CHNT        {
    if (verbose>=2) printf(" CHNT");
    return CHNT;
}
[ ][A-Z]{6}[ ]    {
    yytext[7]=0;
    if (verbose>=2) printf( " airport[%s]", &yytext[1]);
    strcpy(yylval.sval, &yytext[1]);
    /* BEGIN stateTEXT; */
    return AIRPORT;
}
[ ][A-Z]{6} {
    if (verbose>=2) printf( " airport[%s]", &yytext[1]);
    strcpy(yylval.sval, &yytext[1]);
    /* BEGIN stateTEXT; */
    return AIRPORT;
}

<stateSSR>AILO        {
    if (verbose>=2) printf(" ailo");
    return AILO;
}
<stateSSR>AILR        {
    if (verbose>=2) printf(" ailr");
    return AILR;
}
<stateSSR>BIKE        {
    if (verbose>=2) printf(" bike");
    return BIKE;
}
<stateSSR>CCNM     {
    if (verbose>=2) printf(" ccnm");
    BEGIN stateTEXT;
    return CCNM;
}
<stateSSR>CHLD     {
    if (verbose>=2) printf(" chld");
    return CHLD;
}
<stateSSR>CHLN     {
    if (verbose>=2) printf(" chln");
    return CHLN;
}
<stateSSR>CKIN     {
    if (verbose>=2) printf(" ckin");
    return CKIN;
}
<stateSSR>CLID     {
    if (verbose>=2) printf(" clid");
    BEGIN stateRRFARE;
    return CLID;
}
<stateSSR>DOCA     {
    if (verbose>=2) printf(" doca");
    BEGIN stateRRJUNK;
    return DOCA;
}
<stateSSR>DOCO     {
    if (verbose>=2) printf(" doco");
    BEGIN stateRRJUNK;
    return DOCO;
}
<stateSSR>DOCS     {
    if (verbose>=2) printf(" docs");
    BEGIN stateRRJUNK;
    return DOCS;
}
<stateSSR>ECAR     {
    if (verbose>=2) printf(" ecar");
    return ECAR;
}
<stateSSR>EDCO     {
    if (verbose>=2) printf(" edco");
    return EDCO;
}
<stateSSR>FARE     {
    if (verbose>=2) printf(" fare");
    BEGIN stateRRFARE;
    return FARE;
}
<stateSSR>FARX     {
    if (verbose>=2) printf(" farx");
    BEGIN stateRRFARE;
    return FARX;
}
<stateSSR>FLOT     {
    if (verbose>=2) printf(" flot");
    return FLOT;
}
<stateSSR>FOID     {
    if (verbose>=2) printf(" foid");
    BEGIN stateRRJUNK;
    return FOID;
}
<stateSSR>GRPF     {
    if (verbose>=2) printf(" grpf");
    BEGIN stateRRFARE;
    return GRPF;
}
<stateSSR>GRPS     {
    if (verbose>=2) printf(" grps");
    BEGIN stateRRFARE;
    return GRPS;
}
<stateSSR>FQTV     {
    if (verbose>=2) printf(" fqtv");
    BEGIN stateMERDE;
    return FQTV;
}
<stateSSR>INFT     {
    if (verbose>=2) printf(" inft");
    return INFT;
}
<stateSSR>LANG     {
    if (verbose>=2) printf(" lang");
    return LANG;
}
<stateSSR>NSSA     {
    if (verbose>=2) printf(" nssa");
    return NSSA;
}
<stateSSR>NSST     {
    if (verbose>=2) printf(" nsst");
    return NSST;
}
<stateSSR>OTHS     {
    if (verbose>=2) printf(" oths");
    BEGIN stateMERDE;
    return OTHS;
}
<stateSSR>PAXT     {
    if (verbose>=2) printf(" paxt");
    return PAXT;
}
<stateSSR>PCCC     {
    if (verbose>=2) printf(" pccc");
    return PCCC;
}
<stateSSR>RRCA     {
    if (verbose>=2) printf(" rrca");
    BEGIN stateRRSTUF;
    return RRCA;
}
<stateSSR>RRCB     {
    if (verbose>=2) printf(" rrcb");
    BEGIN stateRRSTUF;
    return RRCB;
}
<stateSSR>RRCE     {
    if (verbose>=2) printf(" rrce");
    BEGIN stateRRSTUF;
    return RRCE;
}
<stateSSR>RRCP     {
    if (verbose>=2) printf(" rrcp");
    BEGIN stateRRSTUF;
    return RRCP;
}
<stateSSR>RRTP     {
    if (verbose>=2) printf(" rrtp");
    BEGIN stateRRJUNK;
    return RRTP;
}
<stateSSR>RRTX     {
    if (verbose>=2) printf(" rrtx");
    BEGIN stateRRJUNK;
    return RRTX;
}
<stateSSR>SEAT     {
    if (verbose>=2) printf(" seat");
    return SEAT;
}
<stateSSR>SPEQ     {
    if (verbose>=2) printf(" speq");
    return SPEQ;
}
<stateSSR>TKDG     {
    if (verbose>=2) printf(" tkdg");
    return TKDG;
}
<stateSSR>TKNE     {
    if (verbose>=2) printf(" tkne");
    return TKNE;
}
<stateSSR>TKNM     {
    if (verbose>=2) printf(" tknm");
    BEGIN stateRRJUNK;
    return TKNM;
}
<stateSSR>XBAG     {
    if (verbose>=2) printf(" xbag");
    return XBAG;
}
<stateSSR>VOYG     {
    if (verbose>=2) printf(" voyg");
    BEGIN stateMERDE;
    return VOYG;
}
<stateSSR>[\/]{3}  {
    if (verbose>=2) printf(" ffFSLASH");
    BEGIN stateTEXT;
    return FSLASH;
}
<stateRRJUNK>[\/]{3}  {
    if (verbose>=2) printf(" ffFSLASH");
    BEGIN stateTEXT;
    return FSLASH;
}

<stateRRFARE>(JE|SA|YY) {
    if (verbose>=2) printf(" airline[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateTEXT;
    return AIRLINE;
}

<stateMERDE>(JE|SA) {
    if (verbose>=2) printf(" airline[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateTEXT;
    return AIRLINE;
}

<stateRRJUNK>(JE|SA) {
    if (verbose>=2) printf(" airline[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return AIRLINE;
}
<stateRRJUNK>(HK|KK|SS|XX|CS|CH|HN|UN|TK|CX|CN|UC|NN|HL|PU|LC|LA|HX|NO|RR)[0-9]{1,2}     {
    if (verbose>=2) printf(" junkAction[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateTEXT;
    return ACTION;
}
<stateRRJUNK>VY {
    if (verbose>=2) printf(" airline[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateTEXT;
    return AIRLINE;
}
<stateRRJUNK>CC {
    if (verbose>=2) printf(" airline[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateTEXT;
    return AIRLINE;
}

<stateRRSTUF>(JE|SA) {
    if (verbose>=2) printf(" airline[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return AIRLINE;
}
<stateRRSTUF>(HK|KK|SS|XX|CS|CH|HN|UN|TK|CX|CN|UC|NN|HL|PU|LC|LA|HX|NO|RR)[0-9]{1,2}     {
    if (verbose>=2) printf(" stufAction[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return ACTION;
}

<stateSSR>(JE|SA|YY) {
    if (verbose>=2) printf(" airline[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return AIRLINE;
}
<stateSSR>(HK|KK|SS|XX|CS|CH|HN|UN|TK|CX|CN|UC|NN|HL|PU|LC|LA|HX|NO|RR)[0-9]{1,2}     {
    if (verbose>=2) printf(" ssrAction[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateFLIGHT;
    return ACTION;
}
<stateFLIGHT>[A-Z]{6} {
    if (verbose>=2) printf( " airport[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return AIRPORT;
}
<stateFLIGHT>[0-9]{2,4}                 {
    if (verbose>=2) printf(" number[%s]", yytext);
    yylval.ival = atoi(yytext);
    return NUMBER;
}
<stateFLIGHT>[A-Z][0-3][0-9](JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[0-9]{2}  {
    if (verbose>=2) printf(" flightDatedmy[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return DATEDMY;
}
<stateFLIGHT>[A-Z][0-3][0-9](JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)  {
    if (verbose>=2) printf(" flightDatedm[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return DATEDM;
}
<stateRRSTUF>[-][1-9]+ {
    if (verbose>=2) printf(" paxcount[%s]", &yytext[1]);
    yylval.ival = atoi(&yytext[1]);
    BEGIN statePAXNAME;
    return PAXCOUNT;
}
<stateFLIGHT>[-][1-9]+ {
    if (verbose>=2) printf(" paxcount[%s]", &yytext[1]);
    yylval.ival = atoi(&yytext[1]);
    BEGIN statePAXNAME;
    return PAXCOUNT;
}
<stateFLIGHT>[\.] {
    if (verbose>=2) printf(" dot");
    BEGIN stateTEXT;
    return DOT;
}
<statePAXNAME>[\.] {
    if (verbose>=2) printf(" dot");
    BEGIN stateTEXT;
    return DOT;
}

[123][0-9]{3}\-[012][0-9]\-[0123][0-9]T[012][0-9]:[0-5][0-9]:[0-5][0-9] {
    if (verbose>=2) printf(" dts[%s]", yytext);
    return DTS;
}
[A-Z0-9._%+-]+\/\/[A-Z0-9.-]+\.[A-Z]{2,4} {
    if (verbose>=2) printf(" email[%s]", yytext);
    if ('.' == yytext[0]) strcpy(yylval.sval, &yytext[1]);
    else strcpy(yylval.sval, yytext);
    return EMAIL;
}
[A-Z]{2}[0-3][0-9][A-Z][0-9]{2}[A-Z]{3}[0-9]{2}     {
    if (verbose>=2) printf(" fcd[%s]", yytext);
    return FCD;
}
OSI|OSIJE|OSI[ ]YY   {
    if (verbose>=2) printf(" osi[%s]", yytext);
    BEGIN stateOSI;
    return OSI;
}
<stateOSI>DOB         {
    if (verbose>=2) printf(" dob");
    BEGIN stateTEXT;
    return DOB;
}
<stateOSI>CTCA        {
    if (verbose>=2) printf(" ctca");
    BEGIN stateTEXT;
    return CTCA;
}
<stateOSI>CTCB        {
    if (verbose>=2) printf(" ctcb");
    BEGIN stateTEXT;
    return CTCB;
}
<stateOSI>CTCE        {
    if (verbose>=2) printf(" ctce");
    BEGIN stateTEXT;
    return CTCE;
}
<stateOSI>CTCF        {
    if (verbose>=2) printf(" ctcf");
    BEGIN stateTEXT;
    return CTCF;
}
<stateOSI>CTCH        {
    if (verbose>=2) printf(" ctch");
    BEGIN stateTEXT;
    return CTCH;
}
<stateOSI>CTCM        {
    if (verbose>=2) printf(" ctcm");
    BEGIN stateTEXT;
    return CTCM;
}
<stateOSI>CTCP        {
    if (verbose>=2) printf(" ctcp");
    BEGIN stateTEXT;
    return CTCP;
}
<stateOSI>CTCT        {
    if (verbose>=2) printf(" ctct");
    BEGIN stateTEXT;
    return CTCT;
}
<stateOSI>NXTM        {
    if (verbose>=2) printf(" nxtm");
    BEGIN stateTEXT;
    return NXTM;
}
^\.[A-Z][A-Z0-9]{6}  {
    if (verbose>=2) printf(" commid[%s]", yytext);
    strcpy(yylval.sval, &yytext[1]);
    BEGIN stateCOMMID;
    return COMMID;
}
[BG][0-9]{4,5}  {
    if (verbose>=2) printf(" flight[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return FLIGHT;
}
7B[0-9]{3,4}[A-Z]  {
    if (verbose>=2) printf(" flight[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return FLIGHT;
}
JE[0-9]{3,4}[A-Z]  {
    if (verbose>=2) printf(" flight[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return FLIGHT;
}
[0-3][0-9](JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[0-9][0-9] {
    if (verbose>=2) printf(" datedmy[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return DATEDMY;
}
[0-3][0-9](JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)  {
    if (verbose>=2) printf(" datedm[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return DATEDM;
}
[A-Z]{2}[0-9]{4}[A-Z]    {
    if (verbose>=2) printf(" csflt[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return CSFLT;
}
[A-Z]{2}[0-9]{3}[A-Z]    {
    if (verbose>=2) printf(" flight[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return FLIGHT;
}
[A-Z]{2}[0-9]{2}[A-Z]    {
    if (verbose>=2) printf(" csflt[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return CSFLT;
}
^[1-9][0-9]{0,2} {
    if (verbose>=2) printf(" paxcount1[%s]", yytext);
    yylval.ival = atoi(yytext);
    BEGIN statePAXNAME;
    return PAXCOUNT;
}
<statePAXNAME>[A-Z][A-Z\/ ]+ {
    if (verbose>=2) printf(" paxname[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN statePAXNAME;
    return PAXNAME;
}
<statePAXNAME>[1-9]+ {
    if (verbose>=2) printf(" paxcount[%s]", yytext);
    yylval.ival = atoi(yytext);
    return PAXCOUNT;
}
<stateCOMMID>[A-Z0-9]+ {
    if (verbose>=2) printf(" alnum[%s]", yytext);
    strcpy(yylval.sval, yytext);
    BEGIN stateAIRIMP;
    return ALNUM;
}
    /*
[A-Z]+         {
    printf(" NAME[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return NAME;
}
[(?<!^)A-Z]{3}[A-Z0-9]+      {
    printf(" IDENTIFIER[%s]", yytext);
    strcpy(yylval.sval, yytext);
    return IDENTIFIER;
}
[0-9][A-Z][0-9]{2}  {
    if (verbose>=2) printf(" code[%s]", yytext);
    return CODE;
}
[0-9][A-Z]{2}[0-9]  {
    if (verbose>=2) printf(" code[%s]", yytext);
    return CODE;
}
    */
[0-9]+\.[0-9]{1,7}  {
    if (verbose>=2) printf(" amount[%s]", yytext);
    yylval.dval = atof(yytext);
    return AMOUNT;
}
[0-9]{3}[0-9]+                  {
    if (verbose>=2) printf(" number[%s]", yytext);
    yylval.ival = atoi(yytext);
    return NUMBER;
}
<stateOSI>[-A-Za-z0-9 \/\.\-\|\[\]]+     {
    int i,j;
    if (verbose>=2) printf(" osiText[%s]", yytext);
    j = strlen(yytext);
    for (i=0; i<j; i++)
    {
        if (yytext[i] != ' ' && yytext[i] != '.' && yytext[i] != '-') break;
    }
    strcpy(yylval.sval, &yytext[i]);
    BEGIN stateAIRIMP;
    return TEXT;
}
<stateTEXT>[A-Za-z0-9 :_&,\.\/\*\-\(\)\|\[\]]+   {
    int i,j;
    j = strlen(yytext);
    for (i=0; i<j; i++)
    {
        if (yytext[i] != ' ' && yytext[i] != '.' && yytext[i] != '-') break;
    }
    if (verbose>=2) printf(" text%d[%s]%d", i, yytext, yyleng);
    strcpy(yylval.sval, &yytext[i]);
    BEGIN stateAIRIMP;
    return TEXT;
}

%%
