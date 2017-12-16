#ifndef lint
static const char yysccsid[] = "@(#)yaccpar	1.9 (Berkeley) 02/21/93";
#endif

#define YYBYACC 1
#define YYMAJOR 1
#define YYMINOR 9
#define YYPATCH 20130304

#define YYEMPTY        (-1)
#define yyclearin      (yychar = YYEMPTY)
#define yyerrok        (yyerrflag = 0)
#define YYRECOVERING() (yyerrflag != 0)

#define YYPREFIX "yy"

#define YYPURE 0

#line 2 "read_airimp.y"
#include <stdio.h>
#include <string.h>

#define YYLMAX 10240

/* int yydebug=0;*/
/**/
int verbose;
int airimperr;

extern FILE * yyin;
extern int yylineno;
int yyerrstatus;
extern char * yytext;
#line 18 "read_airimp.y"
#ifdef YYSTYPE
#undef  YYSTYPE_IS_DECLARED
#define YYSTYPE_IS_DECLARED 1
#endif
#ifndef YYSTYPE_IS_DECLARED
#define YYSTYPE_IS_DECLARED 1
typedef union
{
    char sval[1024];
    int ival;
    double dval;
} YYSTYPE;
#endif /* !YYSTYPE_IS_DECLARED */
#line 48 "y.tab.c"

/* compatibility with bison */
#ifdef YYPARSE_PARAM
/* compatibility with FreeBSD */
# ifdef YYPARSE_PARAM_TYPE
#  define YYPARSE_DECL() yyparse(YYPARSE_PARAM_TYPE YYPARSE_PARAM)
# else
#  define YYPARSE_DECL() yyparse(void *YYPARSE_PARAM)
# endif
#else
# define YYPARSE_DECL() yyparse(void)
#endif

/* Parameters sent to lex. */
#ifdef YYLEX_PARAM
# define YYLEX_DECL() yylex(void *YYLEX_PARAM)
# define YYLEX yylex(YYLEX_PARAM)
#else
# define YYLEX_DECL() yylex(void)
# define YYLEX yylex()
#endif

/* Parameters sent to yyerror. */
#ifndef YYERROR_DECL
#define YYERROR_DECL() yyerror(const char *s)
#endif
#ifndef YYERROR_CALL
#define YYERROR_CALL(msg) yyerror(msg)
#endif

extern int YYPARSE_DECL();

#define ADDR 257
#define QK 258
#define QU 259
#define SA 260
#define YY 261
#define ASC 262
#define AVS 263
#define DVD 264
#define NAC 265
#define NCO 266
#define NAR 267
#define NRL 268
#define PDM 269
#define TRL 270
#define ARNK 271
#define RECLOC 272
#define TITLE 273
#define IDENTIFIER 274
#define CHNT 275
#define DOT 276
#define DASH 277
#define NAME 278
#define COMMID 279
#define FLIGHT 280
#define CSFLT 281
#define FLT 282
#define DTS 283
#define AMOUNT 284
#define NUMBER 285
#define ALNUM 286
#define DATEDM 287
#define DATEDMY 288
#define FSLASH 289
#define BSLASH 290
#define ACTION 291
#define SSRCODE 292
#define TKNE 293
#define TKDG 294
#define CKIN 295
#define PAXNUM 296
#define PAXNAME 297
#define PAXCOUNT 298
#define AIRPORT 299
#define OSI 300
#define DOB 301
#define CTCA 302
#define CTCB 303
#define CTCE 304
#define CTCF 305
#define CTCH 306
#define CTCM 307
#define CTCT 308
#define CTCP 309
#define NXTM 310
#define TEXT 311
#define SSR 312
#define AILO 313
#define AILR 314
#define BIKE 315
#define CCNM 316
#define CHLN 317
#define CLID 318
#define DOCA 319
#define DOCO 320
#define DOCS 321
#define ECAR 322
#define EDCO 323
#define FARE 324
#define FARX 325
#define FOID 326
#define FQTV 327
#define FLOT 328
#define GRPF 329
#define GRPS 330
#define INFT 331
#define LANG 332
#define RRTX 333
#define CHLD 334
#define FCD 335
#define NSSA 336
#define OTHS 337
#define PAXT 338
#define PCCC 339
#define RRTP 340
#define RRCA 341
#define RRCB 342
#define RRCE 343
#define RRCP 344
#define EMAIL 345
#define SEAT 346
#define SPEQ 347
#define TKNM 348
#define VOYG 349
#define XBAG 350
#define NSST 351
#define AIRLINE 352
#define EOL 353
#define YYERRCODE 256
static const short yylhs[] = {                           -1,
    0,    0,    0,    0,    1,    1,    1,    1,    1,    1,
    1,    1,    1,    1,    2,    2,    2,   10,    9,    9,
   11,   11,   11,   11,   11,   11,   11,   11,   11,    5,
    5,   21,   21,   21,   21,   21,    7,    7,    8,    8,
    8,   23,   23,   23,   23,   23,   23,   23,   23,   23,
   23,   23,   23,   23,   23,   23,   23,   23,   23,   23,
   23,   23,   23,   23,   23,   23,   23,   23,   23,   23,
   23,   23,   23,   23,   23,   23,   23,   23,   23,   23,
   23,   23,   23,   23,   23,   23,   23,   23,   23,   23,
   23,   23,   23,    3,    3,    3,    4,    6,    6,    6,
    6,   76,   76,   76,   76,   22,   22,   22,   22,   22,
   22,   22,   22,   22,   22,   22,   14,   13,   77,   77,
   12,   16,   15,   18,   17,   19,   24,   24,   20,   26,
   27,   28,   29,   29,   30,   31,   32,   33,   34,   35,
   36,   37,   38,   38,   39,   41,   41,   41,   41,   42,
   43,   43,   43,   43,   43,   43,   43,   43,   44,   45,
   46,   40,   40,   47,   48,   53,   51,   52,   56,   56,
   56,   56,   56,   49,   50,   54,   55,   57,   57,   58,
   59,   60,   61,   62,   63,   64,   65,   66,   67,   68,
   69,   69,   69,   70,   70,   72,   72,   72,   72,   72,
   72,   72,   71,   73,   73,   74,   75,   75,   25,
};
static const short yylen[] = {                            2,
    2,    1,    1,    2,    7,    6,    6,    6,    8,    7,
    7,    5,    5,    3,    2,    1,    0,    1,    2,    1,
    1,    1,    1,    1,    1,    1,    1,    1,    1,    2,
    1,    2,    3,    3,    3,    3,    2,    1,    2,    1,
    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
    1,    1,    1,    2,    3,    3,    3,    2,    5,    3,
    1,    3,    2,    2,    1,    5,    5,    4,    5,    6,
    6,    5,    5,    6,    6,    2,    2,    2,    3,    2,
    2,    2,    2,    2,    2,    2,    3,    3,    2,    4,
    4,    4,    4,    4,    4,    4,    4,    4,    4,    4,
   10,   10,   11,   12,    4,    7,    9,    9,    8,   12,
   12,   12,   12,   12,   12,   10,   10,    9,    5,    6,
    6,    6,    6,    7,    7,    6,    5,    5,   12,   12,
   12,   10,   12,    5,    5,    5,    7,    7,   10,    8,
   10,    5,    9,   12,    9,    9,    8,    9,    6,    6,
   10,   12,   12,    9,   12,    6,   10,   10,   12,   12,
   12,   12,    9,    4,    6,    5,   12,   12,    3,
};
static const short yydefred[] = {                         0,
    0,    0,    0,    0,   18,    0,    2,    0,    0,   16,
    4,   94,    0,    0,    1,   15,    0,    0,   96,   95,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,   41,   20,   21,   22,
   23,   24,   25,   26,   27,   28,   29,   31,   40,   42,
   43,   44,   45,   46,   47,   48,   49,   50,   51,   52,
   53,   54,   55,   56,   57,   58,   59,   60,   61,   62,
   63,   64,   65,   66,   67,   68,   69,   70,   71,   72,
   73,   74,   75,   76,   77,   78,   79,   80,   81,   82,
   83,   84,   85,   86,   87,   88,   89,   90,   91,   92,
   93,   97,  117,  118,  121,  123,  125,  122,  124,  126,
  129,    0,    0,    0,    0,   32,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,   30,   38,
  101,   39,    0,    0,   19,   35,   34,   36,   33,  127,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,  128,    0,    0,    0,  209,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,  116,    0,    0,    0,    0,  104,
    0,    0,    0,    0,   98,    0,    0,   37,    0,    0,
    0,    0,  130,  131,  132,  133,  134,  135,  136,  137,
  139,  138,  140,    0,    0,    0,    0,    0,    0,    0,
  145,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,  204,    0,    0,    0,    0,    0,    0,    0,    0,
    0,  102,    0,  120,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,  159,    0,    0,    0,    0,    0,    0,  174,  175,
    0,  176,    0,  167,  168,    0,    0,    0,    0,    0,
  182,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,  206,    0,    0,    0,    0,    0,    0,    0,  119,
    0,    0,    0,    0,    0,  196,    0,    0,    0,    0,
    0,    0,    0,    0,  160,  161,  162,  163,    0,    0,
  166,    0,    0,    0,    0,  190,    0,    0,    0,    0,
  189,    0,    0,    0,    0,    0,    0,  205,    0,    0,
  109,    0,  107,    0,  106,    0,  113,    0,  112,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,  164,  165,  177,    0,    0,    0,  178,    0,  146,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,  111,  110,  115,  114,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,  149,  180,    0,    0,
    0,    0,  187,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,  203,  158,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,  147,  148,
  183,    0,  185,  186,  188,    0,    0,    0,  194,    0,
    0,    0,    0,  198,    0,  197,    0,  157,    0,    0,
  156,  141,  142,    0,    0,    0,  172,    0,    0,  179,
    0,  191,    0,    0,    0,    0,    0,  181,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,  143,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
  199,  201,  200,  202,  151,  152,  154,  153,  155,  144,
  150,  171,  173,  170,  169,  184,  192,  193,  195,  207,
  208,
};
static const short yydgoto[] = {                          6,
    7,    8,    9,   18,   34,  175,  176,   35,   36,   16,
   38,   39,   40,   41,   42,   43,   44,   45,   46,   47,
   48,  180,   49,   50,   51,   52,   53,   54,   55,   56,
   57,   58,   59,   60,   61,   62,   63,   64,   65,   66,
   67,   68,   69,   70,   71,   72,   73,   74,   75,   76,
   77,   78,   79,   80,   81,   82,   83,   84,   85,   86,
   87,   88,   89,   90,   91,   92,   93,   94,   95,   96,
   97,   98,   99,  100,  101,  181,  256,
};
static const short yysindex[] = {                      -229,
    3, -302, -129, -123,    0,  -54,    0, -188, -111,    0,
    0,    0, -169, -161,    0,    0, -148,  -22,    0,    0,
 -158, -146, -142, -133, -124, -104, -100,  -93,  -76,  -67,
 -227,  124,   51, -165, -126,  141,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,  -66,  -61,  -47,  -46,    0,  -38,  -94,   -7,    7,
 -286,   18,   19,   37,   38,   43,   45,  -37,  -33,   -5,
   -1,  -25,    9,   62,   63,   46,   65,   66,   68,   84,
   85,   86,   87,   88,   89,   90,   91,   92,   93,   94,
   95,   96,   97,   98,   99,  100,  101,  102,  103,  104,
  105,  106,  107,  108,  109, -225,  110,  111,  112,    2,
  -87,  -78,    6,  119, -232, -239, -279,   72,    0,    0,
    0,    0, -215, -234,    0,    0,    0,    0,    0,    0,
   10,   71,  113,  114,  115,  116,  117,  118,  120,  121,
  122,    0, -108,   69,  128,    0,  174,  181,  185,  125,
  186,  168,  189,  190,  -83,  191,  192,  173,  175,  194,
  176,  197,  178,  179,  200,  201,  202,  203,  204,  187,
  205,  206,  208,  209,  210,  211,  212,  213,  214,  153,
  155,  198,  217,  219,    0, -222,  215,  216,  218,    0,
  158, -291, -239, -279,    0,  -73, -279,    0, -188, -239,
  -84, -188,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,  207,  220,  221,  -72,  222,  223,  224,
    0,  225,  159,  226,  227,  228,  229,  230,  231,  160,
  163,  232,  172,  233,  180,  182,  235,  237,  234,  243,
  245,  193,  244,  248,  238,  250,  252,  253,  254,  255,
  256,    0,  242,  236,  257,  258,  259,  240,  268,  269,
  270,    0,  239,    0, -188, -279,    0, -188, -125, -188,
 -279, -239,  241,  277,  278,  267,  280,  281,  282,  283,
  284,    0,  246,  247,  249,  251,  260,  261,    0,    0,
  262,    0,  263,    0,    0,  285, -261,  264,  276,  290,
    0,  279,  292,  265,  286,  287,  288,  289,  293,  294,
  266,    0,  295,  296,  271, -241, -240, -236, -230,    0,
 -188,  -73, -188, -188, -279,    0,  -55,  300,  306,  -53,
  302,  303,  305,  307,    0,    0,    0,    0,  272,  273,
    0,  274,  -51,  301,  275,    0, -260,  309,  321,  310,
    0,  325,  327,  183,  329,  -49,  -36,    0,  -31,  319,
    0,  291,    0,  297,    0,  298,    0,  299,    0, -125,
 -188, -238,  311,  312,  320, -220,  313,  314,  315,  316,
  318,    0,    0,    0, -213,  322,  331,    0, -257,    0,
  304,  323,  324,  326,  328,  308,  330, -167,  332,  334,
  333,  335,  337,  345,    0,    0,    0,    0,  336,  339,
  341,  317,  338,  344,  343,  346,  349,  351,  352,  356,
  347,  357,  358,  348,  340,  342,    0,    0,  350,  359,
  353,  354,    0,  355,  360,  363,  365,  361,  366,  367,
  368,  362,  364, -242,  390,    0,    0,  369,  391, -231,
  370,  371, -130,  392,  372,  393,  396,  373,    0,    0,
    0,  398,    0,    0,    0,  374,  399,  400,    0,  401,
  402,  403,  375,    0, -160,    0, -156,    0, -151, -170,
    0,    0,    0,  376,  377,  378,    0, -136, -121,    0,
  379,    0,  381,  383,  385,  386,  387,    0,  380,  382,
  384,  388,  389,  394,  395,  397,  404,  405,    0,  406,
  407,  408,  409,  410,  411,  412,  413,  414,  415,  416,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,
};
static const short yyrindex[] = {                       526,
    0,    0,    0,    0,    0,    0,    0,   11,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,   14,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0, -118,    0,    0,    0,   17,    0,    0,    0,
    0,    0,    0,   17,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
  -82,    0,   17,   17,    0,    0,   17,    0,   23,    0,
    0,   26,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,   36,   17,    5,   40, -192,   44,
   17,   17,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    8,    0,    0,    0,    0,    0,
   52,    0,   55,   64,   17,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0, -141,
   67,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,
};
static const short yygindex[] = {                         0,
  521, -162,    0,    0,  574, -180,  -30,  -32,  595,    1,
  -24,    0,    0,    0,    0,    0,    0,    0,    0,    0,
  -27, -166,  -35,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
    0,    0,    0,    0,    0, -171, -320,
};
#define YYTABLESIZE 769
static const short yytable[] = {                        182,
   10,  177,  261,  255,   16,  184,  179,  108,  382,  258,
    3,  185,   11,   14,  259,  449,   17,  258,   37,  323,
   32,  262,   13,  404,  194,   12,    1,    2,    3,    4,
  485,  170,   33,  535,   37,    6,  170,  469,  170,    8,
  171,  172,  252,    7,  540,  171,  172,  171,  172,  405,
   12,    5,  112,  486,   11,  474,   31,  113,  195,  470,
   32,  324,  481,   10,  173,  174,    9,   32,  317,  422,
  424,  114,   33,    5,  426,  329,  318,  475,  100,   33,
  428,  173,  174,  115,  482,  240,  258,  100,  100,  255,
  325,  328,  450,  258,  330,  487,   22,   23,   24,   25,
   26,   27,   28,   29,   30,  170,   31,  100,  495,  382,
  536,  423,  425,    5,  171,  172,  427,  566,    5,  100,
    5,  541,  429,    5,  559,  116,  241,   13,  561,   99,
  496,  173,  174,   14,   32,  563,  564,   21,   99,   99,
  567,  182,  254,  257,  253,  544,   33,  260,  545,  252,
  560,  571,  105,  185,  562,  179,  105,  255,   99,  565,
  100,  105,  105,  381,    5,  258,  573,   17,  383,  384,
   99,  173,  174,   32,  572,   37,   37,   10,  105,  105,
  274,  105,  275,   19,   10,   33,  170,    5,  103,  574,
  252,   20,  103,  105,  102,  171,  172,  103,  103,  246,
  247,  430,    2,    3,    4,  286,  103,  287,  248,  249,
  104,   99,  173,  174,  103,  103,  191,  103,  182,  105,
  326,  182,  431,  173,  174,  336,  337,  331,  106,  103,
  332,  432,  433,  436,  437,  445,  446,  458,  459,   22,
   23,   24,   25,   26,   27,   28,   29,   30,  107,   31,
  460,  461,  108,  327,   10,  462,  463,   10,  255,  109,
   37,   16,   16,   16,  108,  108,  108,    3,    3,    3,
   14,   14,   14,   17,   17,   17,  110,   32,  108,   13,
   13,   13,   12,   12,   12,  111,  186,  108,  108,   33,
  182,  187,    6,    6,    6,  182,    8,    8,    8,  385,
    7,    7,    7,  192,   41,  188,  189,  108,    5,    5,
    5,   11,   11,   11,  190,  202,   41,  193,  203,  108,
   10,   10,   10,    9,    9,    9,   10,  206,  196,  197,
    5,   10,  327,   22,   23,   24,   25,   26,   27,   28,
   29,   30,  170,  129,  130,  131,  204,  198,  199,  182,
  205,  171,  172,  200,  245,  201,  210,   16,  250,  276,
  207,  132,  263,  133,  134,  135,  136,  137,  138,  139,
  140,  141,  142,  143,  144,  145,  146,  147,  148,  149,
  150,  151,  152,  153,  154,   10,  155,  156,  157,  158,
  159,  160,  161,  162,  163,    0,  164,  165,  166,  167,
  168,  169,   22,   23,   24,   25,   26,   27,   28,   29,
   30,  170,   31,  208,  209,  251,  211,  212,  277,  213,
  171,  172,  117,  264,  118,  119,  120,  121,  122,  123,
  124,  125,  126,  127,  128,  214,  215,  216,  217,  218,
  219,  220,  221,  222,  223,  224,  225,  226,  227,  228,
  229,  230,  231,  232,  233,  234,  235,  236,  237,  238,
  239,  242,  243,  244,  278,  265,  266,  267,  268,  269,
  270,  279,  271,  272,  273,  280,  282,  281,  283,  284,
  285,  288,  289,  290,  292,  291,  293,  294,  295,  296,
  297,  298,  299,  300,  301,  303,  304,  302,  305,  306,
  307,  308,  309,  310,  311,  312,  313,  315,  314,  316,
  322,  342,  349,  319,  320,  350,  321,  333,  334,  335,
  338,  339,  340,  341,  352,   17,   15,  456,  347,  348,
  376,  353,  354,  356,  355,  357,  343,  344,  345,  346,
  359,  362,  351,  360,  358,  361,  363,  365,  364,  366,
  367,  368,  371,  369,  370,  373,  374,  375,  377,  378,
  379,  387,  388,  389,  390,  391,  392,  393,  394,  403,
  399,  400,  407,  402,  408,  409,  410,  416,  417,  419,
  420,  435,  412,  413,  414,  415,  434,  447,  372,  438,
  439,  380,  440,  386,  441,  451,  452,  453,  395,  396,
  454,  397,  455,  398,  457,  464,  484,  473,  471,  183,
  476,  477,  478,  479,  401,  480,  406,  411,  418,  483,
  502,  490,  472,  421,  442,  443,  444,  448,  178,  497,
  499,  508,  500,  489,  501,  504,  491,  505,  492,  509,
  494,    0,  510,  465,  498,  511,  503,  512,  513,  466,
  467,  468,  514,  516,  517,  522,  488,  515,  518,  527,
  493,  528,  530,  531,  532,  537,  539,  546,  548,  506,
  526,  549,  533,  551,  553,  554,  555,  556,  557,    0,
    0,    0,    0,    0,    0,    0,  568,    0,  570,  575,
  507,  576,  519,  577,  520,  578,  579,  580,    0,    0,
    0,    0,  521,    0,    0,  523,  524,  525,    0,    0,
    0,    0,    0,  529,    0,    0,  534,    0,    0,    0,
    0,  538,  542,  543,  547,  550,  552,  558,    0,  569,
    0,    0,  581,    0,  582,    0,  583,    0,    0,    0,
  584,  585,    0,    0,    0,    0,  586,  587,    0,  588,
    0,    0,    0,    0,    0,    0,  589,  590,  591,  592,
  593,  594,  595,  596,  597,  598,  599,  600,  601,
};
static const short yycheck[] = {                         35,
    0,   34,  183,  175,    0,   36,   34,    0,  329,  176,
    0,   36,   10,    0,  177,  276,    0,  184,   18,  311,
  300,  184,    0,  285,  311,    0,  256,  257,  258,  259,
  288,  271,  312,  276,   34,    0,  271,  276,  271,    0,
  280,  281,  275,    0,  276,  280,  281,  280,  281,  311,
  353,    0,  280,  311,    0,  276,  272,  285,  345,  298,
  300,  353,  276,    0,  297,  298,    0,  300,  291,  311,
  311,  299,  312,  353,  311,  256,  299,  298,  271,  312,
  311,  297,  298,  311,  298,  311,  253,  280,  281,  261,
  253,  254,  353,  260,  257,  353,  262,  263,  264,  265,
  266,  267,  268,  269,  270,  271,  272,  300,  276,  430,
  353,  353,  353,  353,  280,  281,  353,  288,  353,  312,
  353,  353,  353,  353,  285,  353,  352,  257,  285,  271,
  298,  297,  298,  257,  300,  287,  288,  286,  280,  281,
  311,  177,  175,  176,  175,  276,  312,  178,  279,  275,
  311,  288,  271,  178,  311,  183,  275,  329,  300,  311,
  353,  280,  281,  326,  353,  332,  288,  279,  331,  332,
  312,  297,  298,  300,  311,  175,  176,  177,  297,  298,
  289,  300,  291,  353,  184,  312,  271,  353,  271,  311,
  275,  353,  275,  312,  353,  280,  281,  280,  281,  287,
  288,  382,  257,  258,  259,  289,  353,  291,  287,  288,
  353,  353,  297,  298,  297,  298,  311,  300,  254,  353,
  253,  257,  385,  297,  298,  298,  299,  260,  353,  312,
  261,  287,  288,  287,  288,  287,  288,  287,  288,  262,
  263,  264,  265,  266,  267,  268,  269,  270,  353,  272,
  287,  288,  353,  253,  254,  287,  288,  257,  430,  353,
  260,  257,  258,  259,  257,  258,  259,  257,  258,  259,
  257,  258,  259,  257,  258,  259,  353,  300,  271,  257,
  258,  259,  257,  258,  259,  353,  353,  280,  281,  312,
  326,  353,  257,  258,  259,  331,  257,  258,  259,  332,
  257,  258,  259,  311,  300,  353,  353,  300,  257,  258,
  259,  257,  258,  259,  353,  353,  312,  311,  352,  312,
  257,  258,  259,  257,  258,  259,  326,  353,  311,  311,
  353,  331,  332,  262,  263,  264,  265,  266,  267,  268,
  269,  270,  271,  293,  294,  295,  352,  311,  311,  385,
  352,  280,  281,  311,  353,  311,  311,  353,  353,  291,
  352,  311,  353,  313,  314,  315,  316,  317,  318,  319,
  320,  321,  322,  323,  324,  325,  326,  327,  328,  329,
  330,  331,  332,  333,  334,  385,  336,  337,  338,  339,
  340,  341,  342,  343,  344,   -1,  346,  347,  348,  349,
  350,  351,  262,  263,  264,  265,  266,  267,  268,  269,
  270,  271,  272,  352,  352,  297,  352,  352,  291,  352,
  280,  281,  299,  353,  301,  302,  303,  304,  305,  306,
  307,  308,  309,  310,  311,  352,  352,  352,  352,  352,
  352,  352,  352,  352,  352,  352,  352,  352,  352,  352,
  352,  352,  352,  352,  352,  352,  352,  352,  352,  352,
  352,  352,  352,  352,  291,  353,  353,  353,  353,  353,
  353,  291,  353,  353,  353,  291,  291,  353,  311,  291,
  291,  291,  291,  311,  291,  311,  311,  291,  311,  311,
  291,  291,  291,  291,  291,  291,  291,  311,  291,  291,
  291,  291,  291,  291,  291,  353,  352,  291,  311,  291,
  353,  353,  353,  299,  299,  353,  299,  311,  299,  299,
  299,  299,  299,  299,  353,    0,    6,  345,  299,  299,
  291,  299,  353,  299,  353,  299,  311,  311,  311,  311,
  298,  298,  311,  299,  311,  353,  299,  298,  311,  298,
  298,  298,  311,  299,  299,  299,  299,  299,  291,  291,
  291,  285,  285,  297,  285,  285,  285,  285,  285,  285,
  311,  311,  297,  311,  285,  297,  285,  285,  285,  285,
  285,  276,  297,  297,  297,  297,  287,  287,  353,  288,
  288,  353,  288,  353,  288,  287,  276,  288,  353,  353,
  276,  353,  276,  353,  276,  287,  276,  288,  298,   36,
  298,  298,  298,  298,  353,  298,  353,  353,  353,  298,
  276,  298,  311,  353,  353,  353,  353,  353,   34,  298,
  298,  288,  298,  311,  298,  297,  311,  297,  311,  297,
  311,   -1,  297,  353,  311,  297,  311,  297,  297,  353,
  353,  353,  297,  297,  297,  297,  353,  311,  311,  297,
  353,  297,  297,  297,  297,  276,  276,  276,  276,  353,
  311,  276,  311,  276,  276,  276,  276,  276,  276,   -1,
   -1,   -1,   -1,   -1,   -1,   -1,  311,   -1,  311,  311,
  353,  311,  353,  311,  353,  311,  311,  311,   -1,   -1,
   -1,   -1,  353,   -1,   -1,  353,  353,  353,   -1,   -1,
   -1,   -1,   -1,  353,   -1,   -1,  353,   -1,   -1,   -1,
   -1,  353,  353,  353,  353,  353,  353,  353,   -1,  353,
   -1,   -1,  353,   -1,  353,   -1,  353,   -1,   -1,   -1,
  353,  353,   -1,   -1,   -1,   -1,  353,  353,   -1,  353,
   -1,   -1,   -1,   -1,   -1,   -1,  353,  353,  353,  353,
  353,  353,  353,  353,  353,  353,  353,  353,  353,
};
#define YYFINAL 6
#ifndef YYDEBUG
#define YYDEBUG 0
#endif
#define YYMAXTOKEN 353
#if YYDEBUG
static const char *yyname[] = {

"end-of-file",0,0,0,0,0,0,0,0,0,"'\\n'",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"ADDR","QK","QU","SA","YY",
"ASC","AVS","DVD","NAC","NCO","NAR","NRL","PDM","TRL","ARNK","RECLOC","TITLE",
"IDENTIFIER","CHNT","DOT","DASH","NAME","COMMID","FLIGHT","CSFLT","FLT","DTS",
"AMOUNT","NUMBER","ALNUM","DATEDM","DATEDMY","FSLASH","BSLASH","ACTION",
"SSRCODE","TKNE","TKDG","CKIN","PAXNUM","PAXNAME","PAXCOUNT","AIRPORT","OSI",
"DOB","CTCA","CTCB","CTCE","CTCF","CTCH","CTCM","CTCT","CTCP","NXTM","TEXT",
"SSR","AILO","AILR","BIKE","CCNM","CHLN","CLID","DOCA","DOCO","DOCS","ECAR",
"EDCO","FARE","FARX","FOID","FQTV","FLOT","GRPF","GRPS","INFT","LANG","RRTX",
"CHLD","FCD","NSSA","OTHS","PAXT","PCCC","RRTP","RRCA","RRCB","RRCE","RRCP",
"EMAIL","SEAT","SPEQ","TKNM","VOYG","XBAG","NSST","AIRLINE","EOL",
};
static const char *yyrule[] = {
"$accept : airimps",
"airimps : airimps airimp",
"airimps : airimp",
"airimps : blanks",
"airimps : error '\\n'",
"airimp : address commid reclocs paxes flights alines blanks",
"airimp : address commid reclocs paxes flights blanks",
"airimp : address commid reclocs flights alines blanks",
"airimp : address commid reclocs paxes alines blanks",
"airimp : address commid actions reclocs paxes flights alines blanks",
"airimp : address commid actions reclocs paxes flights blanks",
"airimp : address commid reclocs actions flights alines blanks",
"airimp : address commid actions flights blanks",
"airimp : address commid reclocs alines blanks",
"airimp : address commid alines",
"blanks : blanks blank",
"blanks : blank",
"blanks :",
"blank : EOL",
"actions : actions action",
"actions : action",
"action : dvd",
"action : avs",
"action : asc",
"action : nac",
"action : nar",
"action : nco",
"action : nrl",
"action : pdm",
"action : trl",
"reclocs : reclocs recloc",
"reclocs : recloc",
"recloc : RECLOC EOL",
"recloc : RECLOC TEXT EOL",
"recloc : RECLOC NUMBER EOL",
"recloc : RECLOC FLIGHT EOL",
"recloc : RECLOC AIRPORT EOL",
"flights : flights flight",
"flights : flight",
"alines : alines aline",
"alines : aline",
"alines : blank",
"aline : osi",
"aline : ssr",
"aline : dob",
"aline : ctca",
"aline : ctcb",
"aline : ctce",
"aline : ctcf",
"aline : ctch",
"aline : ctcm",
"aline : ctcp",
"aline : ctct",
"aline : nxtm",
"aline : ailo",
"aline : ailr",
"aline : bike",
"aline : ccnm",
"aline : docs",
"aline : chld",
"aline : chln",
"aline : ckin",
"aline : clid",
"aline : doca",
"aline : doco",
"aline : ecar",
"aline : edco",
"aline : fare",
"aline : farx",
"aline : grpf",
"aline : grps",
"aline : foid",
"aline : fqtv",
"aline : flot",
"aline : inft",
"aline : lang",
"aline : nssa",
"aline : nsst",
"aline : oths",
"aline : paxt",
"aline : pccc",
"aline : rrca",
"aline : rrcb",
"aline : rrce",
"aline : rrcp",
"aline : rrtp",
"aline : rrtx",
"aline : seat",
"aline : speq",
"aline : tkdg",
"aline : tkne",
"aline : tknm",
"aline : voyg",
"aline : xbag",
"address : ADDR EOL",
"address : QU ADDR EOL",
"address : QK ADDR EOL",
"commid : COMMID ALNUM EOL",
"paxes : paxes pax",
"paxes : paxes chnt paxes chnt paxes",
"paxes : paxes chnt paxes",
"paxes : pax",
"pax : PAXCOUNT PAXNAME EOL",
"pax : PAXCOUNT PAXNAME",
"pax : PAXNAME EOL",
"pax : PAXNAME",
"flight : FLIGHT DATEDMY AIRPORT ACTION EOL",
"flight : FLIGHT DATEDM AIRPORT ACTION EOL",
"flight : FLIGHT DATEDM ACTION AIRPORT",
"flight : FLIGHT DATEDM ACTION AIRPORT EOL",
"flight : FLIGHT DATEDMY AIRPORT ACTION TEXT EOL",
"flight : FLIGHT DATEDM AIRPORT ACTION TEXT EOL",
"flight : CSFLT DATEDMY AIRPORT ACTION EOL",
"flight : CSFLT DATEDM AIRPORT ACTION EOL",
"flight : CSFLT DATEDMY AIRPORT ACTION TEXT EOL",
"flight : CSFLT DATEDM AIRPORT ACTION TEXT EOL",
"flight : ARNK EOL",
"asc : ASC EOL",
"avs : AVS EOL",
"chnt : CHNT TEXT EOL",
"chnt : CHNT EOL",
"dvd : DVD EOL",
"nar : NAR EOL",
"nac : NAC EOL",
"nrl : NRL EOL",
"nco : NCO EOL",
"pdm : PDM EOL",
"osi : OSI AIRPORT EOL",
"osi : OSI TEXT EOL",
"trl : TRL EOL",
"dob : OSI DOB TEXT EOL",
"ctca : OSI CTCA TEXT EOL",
"ctcb : OSI CTCB TEXT EOL",
"ctce : OSI CTCE TEXT EOL",
"ctce : OSI CTCE EMAIL EOL",
"ctcf : OSI CTCF TEXT EOL",
"ctch : OSI CTCH TEXT EOL",
"ctcm : OSI CTCM TEXT EOL",
"ctcp : OSI CTCP TEXT EOL",
"ctct : OSI CTCT TEXT EOL",
"nxtm : OSI NXTM TEXT EOL",
"ailo : SSR AILO AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME EOL",
"ailr : SSR AILR AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME EOL",
"bike : SSR BIKE AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME COMMID EOL",
"bike : SSR BIKE AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"ccnm : SSR CCNM TEXT EOL",
"chld : SSR CHLD AIRLINE ACTION PAXCOUNT PAXNAME EOL",
"chld : SSR CHLD AIRLINE ACTION PAXCOUNT PAXNAME DOT DATEDMY EOL",
"chld : SSR CHLD AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL",
"chld : SSR CHLD AIRLINE ACTION PAXCOUNT PAXNAME DOT EOL",
"chln : SSR CHLN AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT DATEDM EOL",
"ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT DATEDMY EOL",
"ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT DATEDMY EOL",
"ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL",
"ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME EOL",
"ckin : SSR CKIN AIRLINE ACTION AIRPORT NUMBER DATEDM DOT DATEDMY EOL",
"ckin : SSR CKIN AIRLINE ACTION PAXCOUNT PAXNAME DOT DATEDMY EOL",
"clid : SSR CLID AIRLINE TEXT EOL",
"doca : SSR DOCA AIRLINE ACTION TEXT EOL",
"doco : SSR DOCO AIRLINE ACTION TEXT EOL",
"docs : SSR DOCS AIRLINE FSLASH TEXT EOL",
"docs : SSR DOCS AIRLINE ACTION TEXT EOL",
"ecar : SSR ECAR AIRLINE ACTION AIRPORT TEXT EOL",
"edco : SSR EDCO AIRLINE ACTION AIRPORT TEXT EOL",
"foid : SSR FOID AIRLINE ACTION TEXT EOL",
"grpf : SSR GRPF AIRLINE TEXT EOL",
"grps : SSR GRPS AIRLINE TEXT EOL",
"inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT DATEDMY EOL",
"inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT DATEDMY EOL",
"inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL",
"inft : SSR INFT AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL",
"fare : SSR FARE AIRLINE TEXT EOL",
"farx : SSR FARX AIRLINE TEXT EOL",
"fqtv : SSR FQTV AIRLINE TEXT EOL",
"flot : SSR FLOT AIRLINE ACTION AIRPORT TEXT EOL",
"lang : SSR LANG AIRLINE ACTION AIRPORT TEXT EOL",
"lang : SSR LANG AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL",
"nssa : SSR NSSA AIRLINE ACTION AIRPORT NUMBER DATEDM EOL",
"nsst : SSR NSST AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL",
"oths : SSR OTHS AIRLINE TEXT EOL",
"paxt : SSR PAXT AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL",
"pccc : SSR PCCC AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"rrca : SSR RRCA AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL",
"rrcb : SSR RRCB AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL",
"rrce : SSR RRCE AIRLINE ACTION PAXCOUNT PAXNAME EMAIL EOL",
"rrcp : SSR RRCP AIRLINE ACTION PAXCOUNT PAXNAME DOT TEXT EOL",
"rrtp : SSR RRTP AIRLINE ACTION TEXT EOL",
"rrtx : SSR RRTX AIRLINE ACTION TEXT EOL",
"seat : SSR SEAT AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL",
"seat : SSR SEAT AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL",
"seat : SSR SEAT AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"speq : SSR SPEQ AIRLINE ACTION AIRPORT NUMBER DATEDM TEXT EOL",
"speq : SSR SPEQ AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"tkne : SSR TKNE AIRLINE FSLASH TEXT EOL",
"tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME EOL",
"tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDM DOT TEXT EOL",
"tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT NUMBER EOL",
"tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT NUMBER EOL",
"tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL",
"tkne : SSR TKNE AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"tkdg : SSR TKDG AIRLINE ACTION AIRPORT NUMBER DATEDM TEXT EOL",
"tknm : SSR TKNM TEXT EOL",
"tknm : SSR TKNM AIRLINE AIRLINE TEXT EOL",
"voyg : SSR VOYG AIRLINE TEXT EOL",
"xbag : SSR XBAG AIRLINE ACTION AIRPORT NUMBER DATEDM PAXCOUNT PAXNAME DOT TEXT EOL",
"xbag : SSR XBAG AIRLINE ACTION AIRPORT NUMBER DATEDMY PAXCOUNT PAXNAME DOT TEXT EOL",
"ssr : SSR TEXT EOL",

};
#endif

int      yydebug;
int      yynerrs;

int      yyerrflag;
int      yychar;
YYSTYPE  yyval;
YYSTYPE  yylval;

/* define the initial stack-sizes */
#ifdef YYSTACKSIZE
#undef YYMAXDEPTH
#define YYMAXDEPTH  YYSTACKSIZE
#else
#ifdef YYMAXDEPTH
#define YYSTACKSIZE YYMAXDEPTH
#else
#define YYSTACKSIZE 10000
#define YYMAXDEPTH  500
#endif
#endif

#define YYINITSTACKSIZE 500

typedef struct {
    unsigned stacksize;
    short    *s_base;
    short    *s_mark;
    short    *s_last;
    YYSTYPE  *l_base;
    YYSTYPE  *l_mark;
} YYSTACKDATA;
/* variables for the parser stack */
static YYSTACKDATA yystack;
#line 1003 "read_airimp.y"




#line 871 "y.tab.c"

#if YYDEBUG
#include <stdio.h>		/* needed for printf */
#endif

#include <stdlib.h>	/* needed for malloc, etc */
#include <string.h>	/* needed for memset */

/* allocate initial stack or double stack size, up to YYMAXDEPTH */
static int yygrowstack(YYSTACKDATA *data)
{
    int i;
    unsigned newsize;
    short *newss;
    YYSTYPE *newvs;

    if ((newsize = data->stacksize) == 0)
        newsize = YYINITSTACKSIZE;
    else if (newsize >= YYMAXDEPTH)
        return -1;
    else if ((newsize *= 2) > YYMAXDEPTH)
        newsize = YYMAXDEPTH;

    i = (int) (data->s_mark - data->s_base);
    newss = (short *)realloc(data->s_base, newsize * sizeof(*newss));
    if (newss == 0)
        return -1;

    data->s_base = newss;
    data->s_mark = newss + i;

    newvs = (YYSTYPE *)realloc(data->l_base, newsize * sizeof(*newvs));
    if (newvs == 0)
        return -1;

    data->l_base = newvs;
    data->l_mark = newvs + i;

    data->stacksize = newsize;
    data->s_last = data->s_base + newsize - 1;
    return 0;
}

#if YYPURE || defined(YY_NO_LEAKS)
static void yyfreestack(YYSTACKDATA *data)
{
    free(data->s_base);
    free(data->l_base);
    memset(data, 0, sizeof(*data));
}
#else
#define yyfreestack(data) /* nothing */
#endif

#define YYABORT  goto yyabort
#define YYREJECT goto yyabort
#define YYACCEPT goto yyaccept
#define YYERROR  goto yyerrlab

int
YYPARSE_DECL()
{
    int yym, yyn, yystate;
#if YYDEBUG
    const char *yys;

    if ((yys = getenv("YYDEBUG")) != 0)
    {
        yyn = *yys;
        if (yyn >= '0' && yyn <= '9')
            yydebug = yyn - '0';
    }
#endif

    yynerrs = 0;
    yyerrflag = 0;
    yychar = YYEMPTY;
    yystate = 0;

#if YYPURE
    memset(&yystack, 0, sizeof(yystack));
#endif

    if (yystack.s_base == NULL && yygrowstack(&yystack)) goto yyoverflow;
    yystack.s_mark = yystack.s_base;
    yystack.l_mark = yystack.l_base;
    yystate = 0;
    *yystack.s_mark = 0;

yyloop:
    if ((yyn = yydefred[yystate]) != 0) goto yyreduce;
    if (yychar < 0)
    {
        if ((yychar = YYLEX) < 0) yychar = 0;
#if YYDEBUG
        if (yydebug)
        {
            yys = 0;
            if (yychar <= YYMAXTOKEN) yys = yyname[yychar];
            if (!yys) yys = "illegal-symbol";
            printf("%sdebug: state %d, reading %d (%s)\n",
                    YYPREFIX, yystate, yychar, yys);
        }
#endif
    }
    if ((yyn = yysindex[yystate]) && (yyn += yychar) >= 0 &&
            yyn <= YYTABLESIZE && yycheck[yyn] == yychar)
    {
#if YYDEBUG
        if (yydebug)
            printf("%sdebug: state %d, shifting to state %d\n",
                    YYPREFIX, yystate, yytable[yyn]);
#endif
        if (yystack.s_mark >= yystack.s_last && yygrowstack(&yystack))
        {
            goto yyoverflow;
        }
        yystate = yytable[yyn];
        *++yystack.s_mark = yytable[yyn];
        *++yystack.l_mark = yylval;
        yychar = YYEMPTY;
        if (yyerrflag > 0)  --yyerrflag;
        goto yyloop;
    }
    if ((yyn = yyrindex[yystate]) && (yyn += yychar) >= 0 &&
            yyn <= YYTABLESIZE && yycheck[yyn] == yychar)
    {
        yyn = yytable[yyn];
        goto yyreduce;
    }
    if (yyerrflag) goto yyinrecovery;

    yyerror("syntax error");

    goto yyerrlab;

yyerrlab:
    ++yynerrs;

yyinrecovery:
    if (yyerrflag < 3)
    {
        yyerrflag = 3;
        for (;;)
        {
            if ((yyn = yysindex[*yystack.s_mark]) && (yyn += YYERRCODE) >= 0 &&
                    yyn <= YYTABLESIZE && yycheck[yyn] == YYERRCODE)
            {
#if YYDEBUG
                if (yydebug)
                    printf("%sdebug: state %d, error recovery shifting\
 to state %d\n", YYPREFIX, *yystack.s_mark, yytable[yyn]);
#endif
                if (yystack.s_mark >= yystack.s_last && yygrowstack(&yystack))
                {
                    goto yyoverflow;
                }
                yystate = yytable[yyn];
                *++yystack.s_mark = yytable[yyn];
                *++yystack.l_mark = yylval;
                goto yyloop;
            }
            else
            {
#if YYDEBUG
                if (yydebug)
                    printf("%sdebug: error recovery discarding state %d\n",
                            YYPREFIX, *yystack.s_mark);
#endif
                if (yystack.s_mark <= yystack.s_base) goto yyabort;
                --yystack.s_mark;
                --yystack.l_mark;
            }
        }
    }
    else
    {
        if (yychar == 0) goto yyabort;
#if YYDEBUG
        if (yydebug)
        {
            yys = 0;
            if (yychar <= YYMAXTOKEN) yys = yyname[yychar];
            if (!yys) yys = "illegal-symbol";
            printf("%sdebug: state %d, error recovery discards token %d (%s)\n",
                    YYPREFIX, yystate, yychar, yys);
        }
#endif
        yychar = YYEMPTY;
        goto yyloop;
    }

yyreduce:
#if YYDEBUG
    if (yydebug)
        printf("%sdebug: state %d, reducing by rule %d (%s)\n",
                YYPREFIX, yystate, yyn, yyrule[yyn]);
#endif
    yym = yylen[yyn];
    if (yym)
        yyval = yystack.l_mark[1-yym];
    else
        memset(&yyval, 0, sizeof yyval);
    switch (yyn)
    {
case 4:
#line 140 "read_airimp.y"
	{
    yyerrok;
}
break;
case 32:
#line 184 "read_airimp.y"
	{
    if (verbose) printf("recloc");
    printf("*** Record locator\n");
}
break;
case 33:
#line 190 "read_airimp.y"
	{
    if (verbose) printf("recloc");
    printf("*** Record locator %s ref '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 34:
#line 196 "read_airimp.y"
	{
    if (verbose) printf("recloc");
    printf("*** Record locator %s ref %d\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].ival);
}
break;
case 35:
#line 202 "read_airimp.y"
	{
    if (verbose) printf("recloc");
    printf("*** Record locator %s ref '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 36:
#line 208 "read_airimp.y"
	{
    if (verbose) printf("recloc");
    printf("*** Record locator %s ref '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 94:
#line 279 "read_airimp.y"
	{
    if (verbose) printf("address");
    printf("\n*** Address '%s'\n", yystack.l_mark[-1].sval);
    set_address(yystack.l_mark[-1].sval);
}
break;
case 95:
#line 286 "read_airimp.y"
	{
    if (verbose) printf("address");
    printf("\n*** Address '%s'\n", yystack.l_mark[-1].sval);
    set_address(yystack.l_mark[-1].sval);
}
break;
case 96:
#line 293 "read_airimp.y"
	{
    if (verbose) printf("address");
    printf("\n*** Address '%s'\n", yystack.l_mark[-1].sval);
    set_address(yystack.l_mark[-1].sval);
}
break;
case 97:
#line 300 "read_airimp.y"
	{
    if (verbose) printf("commid");
    printf("*** Communication identifier origin %s ref %s\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 102:
#line 319 "read_airimp.y"
	{
    if (verbose) printf("pax");
    printf("*** Passenger %d '%s'\n", yystack.l_mark[-2].ival, yystack.l_mark[-1].sval);
}
break;
case 103:
#line 325 "read_airimp.y"
	{
    if (verbose) printf("pax");
    printf("*** Passenger %d '%s'\n", yystack.l_mark[-1].ival, yystack.l_mark[0].sval);
}
break;
case 104:
#line 331 "read_airimp.y"
	{
    if (verbose) printf("pax");
    printf("*** Passenger '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 105:
#line 337 "read_airimp.y"
	{
    if (verbose) printf("pax");
    printf("*** Passenger '%s'\n", yystack.l_mark[0].sval);
}
break;
case 106:
#line 366 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-4].sval);
    char fclass = yystack.l_mark[-4].sval[n-1];
    yystack.l_mark[-4].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s airports %s action %s\n", yystack.l_mark[-4].sval, fclass, yystack.l_mark[-3].sval[0], yystack.l_mark[-3].sval[1], &yystack.l_mark[-3].sval[2], yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 107:
#line 375 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-4].sval);
    char fclass = yystack.l_mark[-4].sval[n-1];
    yystack.l_mark[-4].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s airports %s action '%s'\n", yystack.l_mark[-4].sval, fclass, yystack.l_mark[-3].sval[0], yystack.l_mark[-3].sval[1], &yystack.l_mark[-3].sval[2], yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 108:
#line 384 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-3].sval);
    char fclass = yystack.l_mark[-3].sval[n-1];
    yystack.l_mark[-3].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s action '%s' airports %s\n", yystack.l_mark[-3].sval, fclass, yystack.l_mark[-2].sval[0], yystack.l_mark[-2].sval[1], &yystack.l_mark[-2].sval[2], yystack.l_mark[-1].sval, yystack.l_mark[0].sval);
}
break;
case 109:
#line 392 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-4].sval);
    char fclass = yystack.l_mark[-4].sval[n-1];
    yystack.l_mark[-4].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s action '%s' airports %s\n", yystack.l_mark[-4].sval, fclass, yystack.l_mark[-3].sval[0], yystack.l_mark[-3].sval[1], &yystack.l_mark[-3].sval[2], yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 110:
#line 401 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-5].sval);
    char fclass = yystack.l_mark[-5].sval[n-1];
    yystack.l_mark[-5].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s airports %s action '%s%s'\n", yystack.l_mark[-5].sval, fclass, yystack.l_mark[-4].sval[0], yystack.l_mark[-4].sval[1], &yystack.l_mark[-4].sval[2], yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 111:
#line 410 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-5].sval);
    char fclass = yystack.l_mark[-5].sval[n-1];
    yystack.l_mark[-5].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Flight %s class %c date %c%c %s airports %s action '%s%s'\n", yystack.l_mark[-5].sval, fclass, yystack.l_mark[-4].sval[0], yystack.l_mark[-4].sval[1], &yystack.l_mark[-4].sval[2], yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 112:
#line 419 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-4].sval);
    char fclass = yystack.l_mark[-4].sval[n-1];
    yystack.l_mark[-4].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Codeshare flight %s class %c date %c%c %s airports %s action '%s'\n", yystack.l_mark[-4].sval, fclass, yystack.l_mark[-3].sval[0], yystack.l_mark[-3].sval[1], &yystack.l_mark[-3].sval[2], yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 113:
#line 428 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-4].sval);
    char fclass = yystack.l_mark[-4].sval[n-1];
    yystack.l_mark[-4].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Codeshare flight %s class %c date %c%c %s airports %s action '%s'\n", yystack.l_mark[-4].sval, fclass, yystack.l_mark[-3].sval[0], yystack.l_mark[-3].sval[1], &yystack.l_mark[-3].sval[2], yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 114:
#line 437 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-5].sval);
    char fclass = yystack.l_mark[-5].sval[n-1];
    yystack.l_mark[-5].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Codeshare flight %s class %c date %c%c %s airports %s action '%s%s'\n", yystack.l_mark[-5].sval, fclass, yystack.l_mark[-4].sval[0], yystack.l_mark[-4].sval[1], &yystack.l_mark[-4].sval[2], yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 115:
#line 446 "read_airimp.y"
	{
    int n = strlen(yystack.l_mark[-5].sval);
    char fclass = yystack.l_mark[-5].sval[n-1];
    yystack.l_mark[-5].sval[n-1] = 0;
    if (verbose) printf("flight");
    printf("*** Codeshare flight %s class %c date %c%c %s airports %s action '%s%s'\n", yystack.l_mark[-5].sval, fclass, yystack.l_mark[-4].sval[0], yystack.l_mark[-4].sval[1], &yystack.l_mark[-4].sval[2], yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 116:
#line 455 "read_airimp.y"
	{
    if (verbose) printf("flight");
    printf("*** Arrival unknown\n");
}
break;
case 117:
#line 461 "read_airimp.y"
	{
    if (verbose) printf("asc");
    printf("*** Advice of schedule change\n");
}
break;
case 118:
#line 467 "read_airimp.y"
	{
    if (verbose) printf("avs");
    printf("*** Availability status\n");
}
break;
case 119:
#line 473 "read_airimp.y"
	{
    if (verbose) printf("chnt");
    printf("*** Change to name '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 120:
#line 479 "read_airimp.y"
	{
    if (verbose) printf("chnt");
    printf("*** Change to name\n");
}
break;
case 121:
#line 485 "read_airimp.y"
	{
    if (verbose) printf("dvd");
    printf("*** Divided PNR\n");
}
break;
case 122:
#line 491 "read_airimp.y"
	{
    if (verbose) printf("nar");
    printf("*** New arrival\n");
}
break;
case 123:
#line 497 "read_airimp.y"
	{
    if (verbose) printf("nac");
    printf("*** No action taken\n");
}
break;
case 124:
#line 503 "read_airimp.y"
	{
    if (verbose) printf("nrl");
    printf("*** Non return leg\n");
}
break;
case 125:
#line 509 "read_airimp.y"
	{
    if (verbose) printf("nco");
    printf("*** New continuation\n");
}
break;
case 126:
#line 515 "read_airimp.y"
	{
    if (verbose) printf("pdm");
    printf("*** Possible duplicate\n");
}
break;
case 127:
#line 521 "read_airimp.y"
	{
    if (verbose) printf("osi");
    printf("*** Other service information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 128:
#line 527 "read_airimp.y"
	{
    if (verbose) printf("osi");
    printf("*** Other service information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 129:
#line 533 "read_airimp.y"
	{
    if (verbose) printf("trl");
    printf("*** Migrated PNR\n");
}
break;
case 130:
#line 539 "read_airimp.y"
	{
    if (verbose) printf("dob");
    printf("*** Date of birth '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 131:
#line 545 "read_airimp.y"
	{
    if (verbose) printf("ctca");
    printf("*** Contact information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 132:
#line 551 "read_airimp.y"
	{
    if (verbose) printf("ctcb");
    printf("*** Contact information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 134:
#line 559 "read_airimp.y"
	{
    if (verbose) printf("ctce");
    printf("*** Contact email '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 135:
#line 565 "read_airimp.y"
	{
    if (verbose) printf("ctcf");
    printf("*** Contact information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 136:
#line 571 "read_airimp.y"
	{
    if (verbose) printf("ctch");
    printf("*** Contact information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 137:
#line 577 "read_airimp.y"
	{
    if (verbose) printf("ctcm");
    printf("*** Contact information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 138:
#line 583 "read_airimp.y"
	{
    if (verbose) printf("ctcp");
    printf("*** Contact information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 139:
#line 589 "read_airimp.y"
	{
    if (verbose) printf("ctct");
    printf("*** Contact information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 140:
#line 595 "read_airimp.y"
	{
    if (verbose) printf("nxtm");
    printf("*** Contact information '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 141:
#line 604 "read_airimp.y"
	{
    printf("*** Insurance '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s'\n",
           yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-2].ival, yystack.l_mark[-1].sval);
}
break;
case 142:
#line 610 "read_airimp.y"
	{
    printf("*** Insurance '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s'\n",
           yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-2].ival, yystack.l_mark[-1].sval);
}
break;
case 143:
#line 616 "read_airimp.y"
	{
    printf("*** Bicycle '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].ival, yystack.l_mark[-4].sval[0], &yystack.l_mark[-4].sval[1], yystack.l_mark[-3].ival, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 144:
#line 622 "read_airimp.y"
	{
    printf("*** Bicycle '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 145:
#line 628 "read_airimp.y"
	{
    printf("*** Credit card number '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 146:
#line 633 "read_airimp.y"
	{
    printf("*** Child airline '%s' action '%s' passenger %d '%s'\n", yystack.l_mark[-4].sval, yystack.l_mark[-3].sval, yystack.l_mark[-2].ival, yystack.l_mark[-1].sval);
}
break;
case 147:
#line 638 "read_airimp.y"
	{
    printf("*** Child airline '%s' action '%s' passenger %d '%s' date '%s'\n", yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 148:
#line 643 "read_airimp.y"
	{
    printf("*** Child airline '%s' action '%s' passenger %d '%s' date '%s'\n", yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 149:
#line 648 "read_airimp.y"
	{
    printf("*** Child airline '%s' action '%s' passenger %d '%s'\n", yystack.l_mark[-5].sval, yystack.l_mark[-4].sval, yystack.l_mark[-3].ival, yystack.l_mark[-2].sval);
}
break;
case 150:
#line 653 "read_airimp.y"
	{
    printf("*** Checkin stuff '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 151:
#line 659 "read_airimp.y"
	{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 152:
#line 665 "read_airimp.y"
	{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 153:
#line 671 "read_airimp.y"
	{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 154:
#line 677 "read_airimp.y"
	{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 155:
#line 683 "read_airimp.y"
	{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 156:
#line 689 "read_airimp.y"
	{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s'\n",
           yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-2].ival, yystack.l_mark[-1].sval);
}
break;
case 157:
#line 695 "read_airimp.y"
	{
    printf("*** Checkin airline '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n",
           yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-1].sval);
}
break;
case 158:
#line 701 "read_airimp.y"
	{
    printf("*** Checkin airline '%s' action '%s' passenger %d '%s' value '%s'\n",
           yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 159:
#line 707 "read_airimp.y"
	{
    printf("*** Caller ID airline %s value '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 160:
#line 712 "read_airimp.y"
	{
    printf("*** Fubar docs '%s' action '%s' value '%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 161:
#line 717 "read_airimp.y"
	{
    printf("*** Documents airline '%s' action '%s' value '%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 162:
#line 721 "read_airimp.y"
	{
    printf("*** Documents airline '%s' value '%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 163:
#line 725 "read_airimp.y"
	{
    printf("*** Documents airline '%s' action '%s' value '%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 164:
#line 730 "read_airimp.y"
	{
    printf("*** Car hire '%s'\n", yystack.l_mark[-4].sval);
}
break;
case 165:
#line 735 "read_airimp.y"
	{
    printf("*** Edcon '%s'\n", yystack.l_mark[-4].sval);
}
break;
case 166:
#line 740 "read_airimp.y"
	{
    printf("*** Fubar '%s' action '%s' value '%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 167:
#line 745 "read_airimp.y"
	{
    printf("*** Other airline '%s' text '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 168:
#line 750 "read_airimp.y"
	{
    printf("*** Other airline '%s' text '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 169:
#line 755 "read_airimp.y"
	{
    printf("*** Infant name '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 170:
#line 761 "read_airimp.y"
	{
    printf("*** Infant name '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 171:
#line 767 "read_airimp.y"
	{
    printf("*** Infant name '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 172:
#line 773 "read_airimp.y"
	{
    printf("*** Infant name '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n",
           yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-1].sval);
}
break;
case 173:
#line 779 "read_airimp.y"
	{
    printf("*** Infant airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 174:
#line 785 "read_airimp.y"
	{
    printf("*** Fare airline %s value '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 175:
#line 790 "read_airimp.y"
	{
    printf("*** Fare airline %s extra '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 176:
#line 795 "read_airimp.y"
	{
    printf("*** Frequent traveller airline %s value '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 177:
#line 800 "read_airimp.y"
	{
    printf("*** Flight other '%s'\n", yystack.l_mark[-4].sval);;
}
break;
case 178:
#line 805 "read_airimp.y"
	{
    printf("*** Language '%s'\n", yystack.l_mark[-4].sval);
}
break;
case 179:
#line 810 "read_airimp.y"
	{
    printf("*** Language airline '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n",
           yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-1].sval);
}
break;
case 180:
#line 816 "read_airimp.y"
	{
    printf("*** Nasty stuff airline '%s' action '%s' airports '%s' number %04d class %c date %s\n",
           yystack.l_mark[-5].sval, yystack.l_mark[-4].sval, yystack.l_mark[-3].sval, yystack.l_mark[-2].ival, yystack.l_mark[-1].sval[0], &yystack.l_mark[-1].sval[1]);
}
break;
case 181:
#line 822 "read_airimp.y"
	{
    printf("*** Nasty stuff airline '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n",
           yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-1].sval);
}
break;
case 182:
#line 828 "read_airimp.y"
	{
    printf("*** Other airline '%s' text '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 183:
#line 833 "read_airimp.y"
	{
    printf("*** Child airline '%s' action '%s' passenger %d '%s' value '%s'\n", yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 184:
#line 842 "read_airimp.y"
	{
    printf("*** Passenger check airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 185:
#line 848 "read_airimp.y"
	{
    printf("*** RRT airline %s action %s passenger %d '%s' phone '%s'\n", yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 186:
#line 854 "read_airimp.y"
	{
    printf("*** RRT airline %s action %s passenger %d '%s' date of birth '%s'\n", yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 187:
#line 859 "read_airimp.y"
	{
    printf("*** RRT airline %s action %s pax %d '%s' email '%s'\n", yystack.l_mark[-5].sval, yystack.l_mark[-4].sval, yystack.l_mark[-3].ival, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 188:
#line 864 "read_airimp.y"
	{
    printf("*** RRT airline %s action %s passenger %d '%s' phone '%s'\n", yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 189:
#line 869 "read_airimp.y"
	{
    printf("*** RRT airline %s action '%s' price '%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 190:
#line 874 "read_airimp.y"
	{
    printf("*** RRT airline %s action %s extra '%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 191:
#line 880 "read_airimp.y"
	{
    printf("*** Seat airline '%s' action '%s' airports '%s' number %04d class %c date %s value '%s'\n", yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-1].sval);
}
break;
case 192:
#line 886 "read_airimp.y"
	{
    printf("*** Seat airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n", yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 193:
#line 892 "read_airimp.y"
	{
    printf("*** Seat airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n", yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 194:
#line 897 "read_airimp.y"
	{
    printf("*** Sport airline '%s' action '%s'' airports '%s' number %04d class %c date %s equipment '%s'\n", yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].sval, yystack.l_mark[-3].ival, yystack.l_mark[-2].sval[0], &yystack.l_mark[-2].sval[1], yystack.l_mark[-1].sval);
}
break;
case 195:
#line 903 "read_airimp.y"
	{
    printf("*** Sport airline '%s' action '%s'' airports '%s' number %04d class %c date %s passenger %d '%s' equipment '%s'\n", yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 196:
#line 908 "read_airimp.y"
	{
    printf("*** E-Ticket number1 airline '%s' value '%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 197:
#line 914 "read_airimp.y"
	{
    printf("*** E-Ticket number2 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s'\n",
           yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-2].ival, yystack.l_mark[-1].sval);
}
break;
case 198:
#line 920 "read_airimp.y"
	{
    printf("*** E-Ticket number3 airline '%s' action '%s' airports '%s' number %04d class %c date %s number '%s'\n", yystack.l_mark[-7].sval, yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].ival, yystack.l_mark[-3].sval[0], &yystack.l_mark[-3].sval[1], yystack.l_mark[-1].sval);
}
break;
case 199:
#line 926 "read_airimp.y"
	{
    printf("*** E-Ticket number4 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value %d\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].ival);
}
break;
case 200:
#line 932 "read_airimp.y"
	{
    printf("*** E-Ticket number5 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value %d\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].ival);
}
break;
case 201:
#line 937 "read_airimp.y"
	{
    printf("*** E-Ticket number6 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 202:
#line 944 "read_airimp.y"
	{
    printf("*** E-Ticket number7 airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n",
           yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 203:
#line 950 "read_airimp.y"
	{
    printf("*** Ticket airline '%s' action '%s' airports '%s' class %c date %s number '%s'\n", yystack.l_mark[-6].sval, yystack.l_mark[-5].sval, yystack.l_mark[-4].sval, yystack.l_mark[-3].ival, yystack.l_mark[-2].sval[0], &yystack.l_mark[-2].sval[1], yystack.l_mark[-1].sval);
}
break;
case 204:
#line 955 "read_airimp.y"
	{
    printf("*** Ticket number '%s'\n", yystack.l_mark[-1].sval);
}
break;
case 205:
#line 960 "read_airimp.y"
	{
    printf("*** Ticket airline '%s' number '%s%s'\n", yystack.l_mark[-3].sval, yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 206:
#line 965 "read_airimp.y"
	{
    printf("*** Voyager miles airline '%s' value '%s'\n", yystack.l_mark[-2].sval, yystack.l_mark[-1].sval);
}
break;
case 207:
#line 971 "read_airimp.y"
	{
    printf("*** Excess baggage airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n", yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 208:
#line 977 "read_airimp.y"
	{
    printf("*** Excess baggage airline '%s' action '%s' airports '%s' number %04d class %c date %s passenger %d '%s' value '%s'\n", yystack.l_mark[-9].sval, yystack.l_mark[-8].sval, yystack.l_mark[-7].sval, yystack.l_mark[-6].ival, yystack.l_mark[-5].sval[0], &yystack.l_mark[-5].sval[1], yystack.l_mark[-4].ival, yystack.l_mark[-3].sval, yystack.l_mark[-1].sval);
}
break;
case 209:
#line 990 "read_airimp.y"
	{
    if (verbose) printf("ssr");
    printf("*** Junk SSR '%s'\n", yystack.l_mark[-1].sval);
}
break;
#line 1887 "y.tab.c"
    }
    yystack.s_mark -= yym;
    yystate = *yystack.s_mark;
    yystack.l_mark -= yym;
    yym = yylhs[yyn];
    if (yystate == 0 && yym == 0)
    {
#if YYDEBUG
        if (yydebug)
            printf("%sdebug: after reduction, shifting from state 0 to\
 state %d\n", YYPREFIX, YYFINAL);
#endif
        yystate = YYFINAL;
        *++yystack.s_mark = YYFINAL;
        *++yystack.l_mark = yyval;
        if (yychar < 0)
        {
            if ((yychar = YYLEX) < 0) yychar = 0;
#if YYDEBUG
            if (yydebug)
            {
                yys = 0;
                if (yychar <= YYMAXTOKEN) yys = yyname[yychar];
                if (!yys) yys = "illegal-symbol";
                printf("%sdebug: state %d, reading %d (%s)\n",
                        YYPREFIX, YYFINAL, yychar, yys);
            }
#endif
        }
        if (yychar == 0) goto yyaccept;
        goto yyloop;
    }
    if ((yyn = yygindex[yym]) && (yyn += yystate) >= 0 &&
            yyn <= YYTABLESIZE && yycheck[yyn] == yystate)
        yystate = yytable[yyn];
    else
        yystate = yydgoto[yym];
#if YYDEBUG
    if (yydebug)
        printf("%sdebug: after reduction, shifting from state %d \
to state %d\n", YYPREFIX, *yystack.s_mark, yystate);
#endif
    if (yystack.s_mark >= yystack.s_last && yygrowstack(&yystack))
    {
        goto yyoverflow;
    }
    *++yystack.s_mark = (short) yystate;
    *++yystack.l_mark = yyval;
    goto yyloop;

yyoverflow:
    yyerror("yacc stack overflow");

yyabort:
    yyfreestack(&yystack);
    return (1);

yyaccept:
    yyfreestack(&yystack);
    return (0);
}
