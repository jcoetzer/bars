INCS = -g -m32 -I.. -I../../../src -I/usr/local/include/gef
CFLAGS = -I$(INFORMIXDIR)/incl/esql $(INCS)

ESQL = $(INFORMIXDIR)/bin/esql
LDFLAGS = =L . -L$(INFORMIXDIR)/lib -L$(INFORMIXDIR)/lib/esql $(shell $(ESQL) -libs | xargs) -lcurl

# YACCDEBUG = -t
YACCDEBUG = --debug --verbose

all: read_airimp libairimp.so

clean :
	rm -f $(RAOBJS) $(LAOBJS)
	rm -f TYPEBALOG.* core.* testairimp
	rm -f read_airimp_lex.c read_airimp.tab.c read_airimp.tab.h read_airimp.output
	rm -f read_airimp libairimp.so

LAOBJS = read_airimp_yacc.o read_airimp_lex.o airimp_data.o
RAOBJS = read_airimp_data.o

read_airimp : Makefile $(RAOBJS) libairimp.so
	gcc -L . -m32 -o read_airimp $(RAOBJS) -lfl -lairimp

# read_airimp : Makefile $(RAOBJS) $(LAOBJS)
# 	gcc -L . -m32 -o read_airimp $(RAOBJS) $(LAOBJS) -lfl

libairimp.so : $(LAOBJS)
	gcc -m32 -shared -o libairimp.so $(LAOBJS)

read_airimp_lex.o : read_airimp_lex.c
	gcc $(INCS) -c -o read_airimp_lex.o read_airimp_lex.c

read_airimp_lex.c : read_airimp.l
	flex -o read_airimp_lex.c read_airimp.l

read_airimp_yacc.o : read_airimp.tab.c
	gcc $(INCS) -c -o read_airimp_yacc.o read_airimp.tab.c

read_airimp.tab.c : read_airimp.y
	bison $(YACCDEBUG) -d read_airimp.y

airimp.o : airimp.c
	gcc $(INCS) -c -o airimp.o airimp.c

testairimp.o : testairimp.c
	gcc $(INCS) -c -o testairimp.o testairimp.c

read_airimp.o : read_airimp.c
	gcc $(INCS) -c -o read_airimp.o read_airimp.c

airimp_data.o : airimp_data.c airimp_data.h
	gcc $(INCS) -c -o airimp_data.o airimp_data.c

