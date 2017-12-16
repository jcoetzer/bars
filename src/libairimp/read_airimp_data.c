
#include <stdio.h>
#include <string.h>

#include "airimp_data.h"

#define YYLMAX 10240

int main(int argc, char **argv)
{
    int n=1;
    char ifname[256] = { 0 };
    char * data;
    int airimperr;
    int verbose;

    verbose=0;

    while (n < argc)
    {
        if (! strcmp(argv[n], "-v")) verbose = 1;
        else if (! strcmp(argv[n], "-vv")) verbose = 2;
        else if (! strcmp(argv[n], "-vvv")) verbose = 3;
        else if (! strcmp(argv[n], "-V")) verbose = 2;
        else if (! strcmp(argv[n], "-d")) verbose = 3;
        else strcpy(ifname, argv[n]);
        ++n;
    }

    init_airimp();

    set_verbose(verbose);

    airimperr = read_airimp(ifname, &data);

    printf("Address : %s\n", data);

    return airimperr;
}
