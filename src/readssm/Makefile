
INCS = -g -I.. -I../../../src -I/usr/local/include/gef
WFLAG = -Wall -Wno-unused-but-set-variable
DFLAG = -O0 -D_DEBUG -DNOTUX -D_PROCSSM

CFLAGS = -I/usr/include/postgresql $(INCS) $(WFLAG)
SRC_PATH=../../../src

CWARN = -Wall

CCC = /usr/bin/g++
ESQL = ecpg -C INFORMIX


PGFLAGS = -I/usr/include/postgresql -I/usr/include
PLFLAGS = -lecpg -lecpg_compat -lpq

CFLAGS = -g $(CWARN) -O


YACCDEBUG = --debug --verbose

all: ssmread ssmwrite

install: ssmread ssmwrite

clean :
	rm -f $(WOBJS) $(ROBJS) $(COBJS)
	rm -f core.* readssm.output
	rm -f readssm_lex.c readssm.tab.c readssm.tab.h readssm.c
	rm -f ssmwrite ssmread
	rm -rf html/

docs: Doxyfile
	doxygen Doxyfile

install: ssmread ssmwrite
	rm -f /opt/bars/bin/core.*
	cp ssmread ssmwrite /opt/bars/bin/

ROBJS = readssm_yacc.o readssm_lex.o ReadSsmFile.o
WOBJS = WriteSsm.o WriteSsmFile.o SsmDate.o
# SsmUtils.o

ssmwrite : Makefile $(WOBJS)
	g++ $(WFLAG) -o ssmwrite $(WOBJS)

ssmread : readssm.tab.h Makefile $(ROBJS)
	g++ $(WFLAG) -o ssmread $(ROBJS) -lfl

ReadSsmFile.o : Makefile ReadSsmFile.cpp ReadSsmFile.h
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o ReadSsmFile.o ReadSsmFile.cpp

readssm_lex.o : Makefile readssm_lex.c
	gcc $(INCS) -c -o readssm_lex.o readssm_lex.c

readssm_lex.c : Makefile readssm.l
	flex -o readssm_lex.c readssm.l

readssm_yacc.o : Makefile readssm.tab.c
	gcc $(INCS) -c -o readssm_yacc.o readssm.tab.c

readssm.tab.h: readssm.tab.c

readssm.tab.c : Makefile readssm.y
	bison $(YACCDEBUG) -d readssm.y

SsmUtils.o : Makefile WriteSsm.cpp
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o SsmUtils.o SsmUtils.cpp

WriteSsm.o : Makefile WriteSsm.cpp
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o WriteSsm.o WriteSsm.cpp

WriteSsmFile.o : Makefile WriteSsmFile.cpp
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o WriteSsmFile.o WriteSsmFile.cpp
