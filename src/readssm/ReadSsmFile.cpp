/**
 * @file ReadSsmFile.cpp
 *
 * Read SSM file and display
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <libgen.h>
#include <stdio.h>
#include <string.h>

extern int yylineno;
extern char * yytext;

int verbose = 0;
int yydebug=0;
int readasm=0;

extern FILE * yyin;

FILE * ssmlog;


extern "C"
{
    /**
     * Parse input data
     *
     * @return zero upon success otherwise non-zero
     */
    int yyparse();
}

/**
 * Display help message
 *
 * @param pname     file name
 */
void show_usage(char * pname);


/**
 * Display build information
 *
 * @param pname     file name
 */
void show_version(char * pname);


/**
 * The big cheese
 *
 * @param argc number of arguments
 * @param argv argument values
 *
 * @return zero upon success otherwise non-zero
 */
int main(int argc, char **argv)
{
    int i, rc;
    char ifname[256] = { 0 };
    char outfnam[128] = { 0 };

    verbose = 0;
    ssmlog = stdout;

    i = 1;
    rc = argc;
    while ( i < argc )
    {
        if ( 0 == strcmp(argv[i], "-h") || 0 == strncmp(argv[i], "--h", 3))
        {
            show_usage(argv[0]);
        }
        else if ( 0 == strncmp(argv[i], "--v", 3) )
        {
            show_version(argv[0]);
        }
        else if ( 0 == strcmp(argv[i], "-q") )
        {
            verbose = 0;
        }
        else if ( 0 == strcmp(argv[i], "-V") )
        {
            verbose = 3;
        }
        else if ( 0 == strcmp(argv[i], "-v") )
        {
            verbose = 2;
        }
        else if ( 0 == strcmp(argv[i], "-y") )
        {
            yydebug = 1;
        }
        else if ( 0 == strcmp(argv[i], "-O") )
        {
            ++i;
            if ( i >= argc ) break;
            strcpy(outfnam, argv[i]);
            if ( verbose>=2 ) printf("Write output file %s\n", outfnam);
        }
        else if ( 0 == strcmp(argv[i], "--asm") )
        {
            readasm = 1;
        }
        else
        {
            strcpy(ifname, argv[i]);
            if ( verbose>=2 ) printf("Read input file %s\n", ifname);
        }
        ++i;
    }

    if ( ifname[0] )
    {
        yyin = fopen(ifname, "r");
        if ( NULL == yyin )
        {
            fprintf(stderr, "Could not read file %s\n", ifname);
            return 1;
        }
    }

    rc = yyparse();
    if ( verbose ) printf("\n");
    if ( rc )
    {
        fprintf(stderr, "\nCould not parse input data\n");
        return rc;
    }

    if ( ifname[0] )
    {
        fclose(yyin);
    }

    return rc;
} // main()


// Display build information
void show_version(char * pname)
{
    fprintf(stderr, "%s :\n", basename(pname));
    fprintf(stderr, "\tRead flight data (version 1.0.0)\n");
    exit(1);
} // show_version()


// Display help message
void show_usage(char * pname)
{
    fprintf(stderr, "Read file and check syntax (version 1.0.0) :\n");
    fprintf(stderr, "\t%s [-v] [<IFILE>]\n", basename(pname));
    fprintf(stderr, "where\n");
    fprintf(stderr, "\t-v\t\tAdditional output\n");
    fprintf(stderr, "\t-y\t\tYacc debug output\n");
    //? fprintf(stderr, "\t-O <OFILE>\tOutput file name (specify '-' for standard output)\n");
    fprintf(stderr, "\t<IFILE>\t\tInput file name (default is standard input)\n");
    exit(1);
} // show_usage()

