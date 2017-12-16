
#include <stdio.h>
#include <string.h>

extern int verbose;
extern int yydebug;

extern FILE * yyin;
extern int airimperr;

#include "airimp_data.h"

struct airimp_data AirimpRec;

int yyparse();

int yywrap(void)
{
    return 1;
}

void init_airimp()
{
    memset(&AirimpRec, 0, sizeof(struct airimp_data));
}

void set_address(char * address)
{
    strcpy(AirimpRec.address, address);
}

char * get_address()
{
    return AirimpRec.address;
}


void set_commid(char * origin, char * ref)
{
    strcpy(AirimpRec.commid_origin, origin);
    strcpy(AirimpRec.commid_ref, ref);
}

char * get_commid_origin()
{
    return AirimpRec.commid_origin;
}

char * get_commid_ref()
{
    return AirimpRec.commid_ref;
}

void set_verbose(int v)
{
    verbose = v;
    if (v >= 3) yydebug = 1;
}

int read_airimp(char * ifname, char ** data)
{
    int n=1;

    if (ifname[0])
    {
        yyin = fopen(ifname, "r");
        if (NULL == yyin)
        {
            fprintf(stderr, "Could not read file %s\n", ifname);
            return 1;
        }
    }

    yyparse();

    if (ifname[0])
    {
        fclose(yyin);
    }

    *data = get_address();

    return airimperr;

}


