#!/usr/local/bin/python
#
# @file SsmYacc.py
#

import sys
import ply.lex as lex
import ply.yacc as yacc

from SsmLex import tokens
#import SsmLex
import SsmData


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

def p_ssmfile(p):
    'asmfile : asmfile alines'
    pass


def p_alines(p):
    '''alines : alines aline
              | aline'''
    pass


def p_aline(p):
    '''aline    : addresses
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
                | classes'''
    pass


def p_addresses(p) :
    '''addresses : addresses addressel
                 | addressel'''
    pass

def p_addressel(p) :
    'addressel : ADRES'
    pass

def p_sender(p):
    'sender : DOT ADRES NUMBER'
    print "*** Sender element: %s" % p[1];

def p_sender2(p):
    'sender : DOT ADRES'
    print "*** Sender element: %s" % (p[2])


def p_mtype(p):
    'mtype : MTYPE'
    print "*** Message type: %s" % (p[1])


def p_ttype(p):
    'ttype : MTIME'
    print "*** Time type: %s" % (p[1])
    set_time_zone(p[1])


def p_configs(p):
    '''configs : configs config
               | config'''
    pass

def p_config(p):
    'config : ACONFIG'
    print "*** Config: %s" % (p[1])
    add_config(p[1])


def p_equip(p):
    'equip : STYPE AIRCRFT PAXBOOK configs'
    print "*** Equipmen1: type %s aircraft %s book %s" % (p[1], p[2], p[3])
    add_equipment(p[2], p[3], "", "")


def p_equip4(p):
    'equip : STYPE AIRCRFT PAXBOOK configs TAIL'
    print "*** Equipmen2: type %s aircraft %s book %s tail %s" % (p[1], p[2], p[3], p[5])
    add_equipment(p[2], p[3], "", p[5])


def p_equip5(p):
    'equip : STYPE AIRCRFT PAXBOOK configs SEGMENT TAIL'
    print "*** Equipmen3: type %s aircraft %s book %s data %s tail %s" % (p[1], p[2], p[3], p[5], p[6])
    add_equipment(p[2], p[3], p[5], p[6])


def p_action(p):
    '''action   : ACTION'''
    pass


def p_period(p):
    'period : DATEDM DATEDM FREQ'
    print "*** Period: from %s to %s (days %d)" % (p[1], p[2], p[3])
    if (add_dates_freq(p[1], p[2], p[3])):
        return 1


def p_flight2(p):
    'flight : FLIGHT AIRLINE'
    print "*** Flight: number %s airline %s" % (p[1], p[2])
    add_flight_number(p[1], p[2])


def p_flight(p):
    'flight : FLIGHT'
    print "*** Flight: number '%s'" % (p[1])
    add_flight_number(p[1], "")


def p_leg(p):
    'leg : LEGSTN LEGSTN'
    print "*** Leg: from %s to %s" % (p[1], p[2])
    add_leg(p[1], p[2], 0)


def p_leg32(p):
    'leg : LEGSTN LEGSTN FREQ'
    print "*** Leg: from %s to %s (%d)" % (p[1], p[2], p[3])
    add_leg(p[1], p[2], p[3])


def p_leg(p):
    'leg : SEGMENT SEGMENT'
    print "*** Leg: from %s to %s (%d)" % (p[1], p[2])
    add_leg(p[1], p[2], 0)


def p_segment(p):
    'segment : SEGMENT COUNT SEGDATA'
    dep = p[1][:3]
    arr = p[1][3:]
    print "*** Segment 3: depart %s arrive %s code %d data %s" % (dep, arr, p[2], p[3])
    add_segment(dep, arr, p[2], p[3])


def p_classes(p):
    'classes : STYPE SEGMENT'
    print "*** Class: type %s data %s" % (p[1], p[2])


def p_classes3(p):
    'classes : STYPE COUNT SEGMENT'
    dep = p[1][0:3]
    arr = p[1][3:]
    print "*** Class: type %s code %d data %s" % (p[1], p[2], p[3])
    add_segment(dep, arr, p[2], p[3])


def p_classes1(p):
    'classes : SEGMENT'
    n = len(p[1])
    # Ignore blanks
    if (n > 0):
        print "*** Class: data '%s' %d bytes" % (p[1], n)
        add_segment("", "", 0, p[1])


def p_commid(p):
    'commid : DOT COMMID NUM6'
    print "*** Communication: %s 06d" % (p[2], p[3])


# Build the parser
#parser = yacc.yacc()

#while True:
   #try:
       #s = raw_input('calc > ')
   #except EOFError:
       #break
   #if not s: continue
   #result = parser.parse(s)
   #print(result)


def usage():
    print "Help!"
    sys.exit(1)


# Pythonic entry point
def main(argv):

    global verbose
    fname = None

    if len(argv) < 1:
        usage()

    for opt in argv:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '-v':
            verbose = 1
        #elif opt == '-I' or opt == '--input':
            #fname = str(arg)
        else:
            fname = str(opt)
            print "read '%s'" % fname

    if fname is None or len(fname)==0:
        print "No input file specified"
        return 1

    print "read '%s'" % fname

    #f = open('/home/johanc/github/MangoGEF/support/src/readssm/data/JE123.31JUL2017.EQT.ssm','r')
    f = open(fname)
    message = f.read()
    #print(message)
    f.close()

    print "go"

    # Build the parser
    parser = yacc.yacc()

    result = parser.parse(message)
    print(result)

    print "done"

    return 0


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)
