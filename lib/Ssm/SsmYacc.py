"""
Parse SSM input.

@file SsmYacc.py
"""

import sys
import ply.lex as lex
import ply.yacc as yacc

from Ssm.SsmLex import tokens
from Ssm.SsmData import SsmData, \
    set_action, \
    set_time_zone, \
    add_flight_number, \
    add_leg, \
    add_dates_freq, \
    add_segment, \
    add_config, \
    add_equipment, \
    read_ssm_data

from BarsLog import blogger, init_blogger

# Error rule for syntax errors
def p_error(p):
    blogger().error("Syntax error in input!")


def p_alines(p):
    '''alines : alines aline
              | aline'''
    #blogger().info("Lines")


def p_aline(p):
    '''aline    : addresses
                | sender
                | sender2
                | mtype
                | ttype
                | action
                | flight
                | flight2
                | flight3
                | flight4
                | period
                | leg
                | leg2
                | equip
                | equip2
                | segment
                | classes
                | classes1
                | blank'''
    #blogger().info("Line")


def p_addresses(p) :
    '''addresses : addresses addressel
                 | addressel'''
    blogger().info("Addresses %s" % p)


def p_addressel(p) :
    'addressel : ADRES EOL'
    blogger().info("Address: %s" % p[1])


def p_sender(p):
    'sender : DOT ADRES SSMREF EOL'
    blogger().info("*** Sender element: %s %s" % (p[2], p[3]))


def p_sender2(p):
    'sender2 : DOT ADRES EOL'
    blogger().info("*** Sender element: %s" % (p[2]))


def p_mtype(p):
    'mtype : MTYPE EOL'
    blogger().info("*** Message type: %s" % (p[1]))


def p_ttype(p):
    'ttype : MTIME EOL'
    blogger().info("*** Time type: %s" % (p[1]))
    set_time_zone(p[1])

# --- action ---

def p_action(p):
    '''action   : ACTION'''
    blogger().info("Action %s" % p[1])
    set_action(p[1])

# --- flight ---

#def p_fdatas(p):
    #'''fdatas : fdatas fdata
              #| fdata'''

#def p_fdata(p):
    #'fdata : ITEMDATA'
    #blogger().info("Flight data %s" % p[1])

def p_flight(p):
    'flight : FLTNUM EOL'
    blogger().info("*** Flight: number '%s'" % (p[1]))
    add_flight_number(p[1], "")

def p_flight2(p):
    'flight2 : FLTNUM ITEMDATA EOL'
    blogger().info("*** Flight: number '%s' %s" % (p[1], p[2]))
    add_flight_number(p[1], p[2])

def p_flight3(p):
    'flight3 : FLTNUM ITEMDATA ITEMDATA EOL'
    blogger().info("*** Flight: number '%s' %s %s" % (p[1], p[2], p[3]))
    add_flight_number(p[1], p[2], p[3])

def p_flight4(p):
    'flight4 : FLTNUM ITEMDATA ITEMDATA ITEMDATA EOL'
    blogger().info("*** Flight: number '%s' %s %s %s" % (p[1], p[2], p[3], p[4]))
    add_flight_number(p[1], p[2], p[3], p[4])

def p_flight_error(p):
    'flight : error'
    blogger().error("Error in flight '%s'" % (p[1]))

#def p_flight2(p):
    #'flight2 : FLTNUM fdatas EOL'
    #blogger().info("*** Flight: number %s airline %s" % (p[1], p[2]))
    #add_flight_number(p[1], p[2])

# --- period ---

def p_period(p):
    'period : DATE DATE FREQ EOL'
    blogger().info("*** Period: from %s to %s (days %s)" % (p[1], p[2], p[3]))
    add_dates_freq(p[1], p[2], p[3])

# --- equip ---

def p_equip(p):
    'equip : STYPE AIRCRFT PAXBOOK DOT CLASS TAIL EOL'
    blogger().info("*** Equipment: type %s aircraft %s booking %s tail %s class %s" % (p[1], p[2], p[3], p[6], p[5]))
    add_equipment(p[2], p[3], p[6], p[5])

def p_equip2(p):
    'equip2 : STYPE AIRCRFT PAXBOOK DOT CLASS CLASS TAIL EOL'
    blogger().info("*** Equipment: type %s aircraft %s booking %s tail %s class %s class %s" % (p[1], p[2], p[3], p[7], p[5], p[6]))
    add_equipment(p[2], p[3], p[7], p[5], p[6])

def p_error_equip(p):
    blogger().error("Syntax error in equip")

# --- leg ---

def p_leg(p):
    'leg : LEGSTN LEGSTN EOL'
    blogger().info("*** Leg: from %s to %s" % (p[1], p[2]))
    add_leg(p[1], p[2], 0)


def p_leg2(p):
    'leg2 : LEGSTN LEGSTN FREQ EOL'
    blogger().info("*** Leg2: from %s to %s (%d)" % (p[1], p[2], int(p[3])))
    add_leg(p[1], p[2], p[3])

# --- segment ---

def p_segment(p):
    'segment : SEGMENT ITEMDATA EOL'
    deparr = p[1]
    blogger().info("*** Segment 3: depart/arrive %s data %s" % (p[1], p[2]))
    add_segment(p[1], p[2])

# --- blank ---

def p_blank(p):
    'blank : EOL'
    pass

# --- classes ---

def p_classes(p):
    'classes : STYPE SEGMENT EOL'
    blogger().info("*** Class: type %s data %s" % (p[1], p[2]))


def p_classes1(p):
    'classes1 : SEGMENT EOL'
    n = len(p[1])
    # Ignore blanks
    if (n > 0):
        blogger().info("*** Class: data '%s' %d bytes" % (p[1], n))
        add_segment("", "", 0, p[1])


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


def YaccFile(fname):
    if fname == "-":
        message = sys.stdin.read()
    else:
        blogger().info("Read '%s'" % fname)

        #f = open('/home/johanc/github/MangoGEF/support/src/readssm/data/JE123.31JUL2017.EQT.ssm','r')
        f = open(fname)
        message = f.read()
        #print(message)
        f.close()

    try:
        # Build the parser
        parser = yacc.yacc()

        #result =
        parser.parse(message)
        blogger().info("parsed")
        #print(result)

    except TypeError as e:
        blogger().error("Parser failed : %s" % str(e))

    return 0


def usage():
    print("Help!")
    sys.exit(1)


# Pythonic entry point
def main(argv):

    global verbose
    fname = None

    if len(argv) < 1:
        usage()
    init_blogger("bars")
    for opt in argv:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '-v':
            _levelsetLevel(logging.INFO)
        elif opt == '-V':
            _levelsetLevel(logging.DEBUG)
        #elif opt == '-I' or opt == '--input':
            #fname = str(arg)
        else:
            fname = str(opt)
            blogger().info("read '%s'" % fname)

    if fname is None or len(fname)==0:
        blogger().error("No input file specified")
        return 1

    rc = YaccFile(fname)

    return rc


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)
