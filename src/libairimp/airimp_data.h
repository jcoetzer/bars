#ifndef AIRIMP_DATA_H
#define AIRIMP_DATA_H

struct airimp_data
{
char recloc[16];
char address[16];
char commid_origin[64];
char commid_ref[64];
int totalpax;
int paxcount[64];
char paxname[64][64];
char flight[8][8];
char fdate[8][8];
char airport[8][8];
char action[8][8];
char fclass[8];
};

void init_airimp();

void set_address(char * address);
void set_commid(char * origin, char * ref);

char * get_commid_origin();

char * get_commid_ref();

void add_pax(int paxcount, char * paxname);

char * get_address();

void set_verbose(int v);

int read_airimp(char * ifname, char ** data);

#endif
