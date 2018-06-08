#!/usr/bin/python


import sys
import getopt
from BarsLog import printlog, set_verbose

import ply.lex as lex
from Ssm.SsmLex import *


#import SsmLex

#def SsmLexer():
    #states = (
    #('equip','inclusive'),
    #('legs','inclusive'),
    #('classes','exclusive')
    #)

    #tokens = (
        #'SPACE',
        #'EOL',
        #'DOT',
        #'SLASH',
        #'SSMQK',
        #'SSMADDRESS',
        ##'SSMSENDER',
        #'SSMREF',
        #'SSMASM',
        #'SSMTIME',
        #'SSMTYPE',
        #'XASM',
        #'FLTNUM',
        #'DATE',
        #'NUMBER',
        #'SSMXX',
        #'SSMJ',
        #'AIRCRAFT',
        #'CLASS',
        #'VVM',
        #'TAIL',
        #'ITEM',
        #'ITEMDATA',
        #'ITENARY',
        #'DATA'
        ##'FLIGHTINFO'
    #)

    #mtype = None
    #verbose = 0

    #t_SPACE = r'[ ]'

    #t_EOL = r'[\n]'

    #t_DOT = r'[\.]'

    #t_SLASH = r'[\/]'

    #def t_SSMJ(t):
        #r'[J][\ ]'
        #t.lexer.begin('equip')
        #return t

    #def t_equip_EOL(t):
        #r'[\n]'
        #t.lexer.begin('legs')
        #return t

    #def t_equip_AIRCRAFT(t):
        #r'[0-9][A-Z0-9]{2}'
        #return t

    #def t_DATA(t):
        #r'[\/][A-Z1-9]*'
        #return t

    #t_equip_SSMXX = r'[X]{2}'

    #def t_equip_DOT(t):
        #r'[\.]'
        #t.lexer.begin('classes')
        #return t

    #def t_classes_CLASS(t):
        #r'[A-Z][0-9]{1,3}'
        #return t

    #def t_classes_end(t):
        #r'VVM|\n'
        #t.lexer.begin('equip')

    #def t_equip_NUMBER(t):
        #r'[0-9]{2}'
        #return t

    #def t_equip_TAIL(t):
        #r'ZS[A-Z]{3}'
        #return t

    #t_SSMQK = r'QK'

    #t_SSMADDRESS = r'[A-Z][A-Z0-9]{5,6}'

    ##t_SSMSENDER = r'\.[A-Z][A-Z0-9]{6}[\ ][0-9]{6}'
    ##t_SSMSENDER = r'((\.[A-Z]([A-Z0-9]{6})((\ ([0-9]{6}))*))|([A-Z]([A-Z]{6})\ ([A-Z]{2}\/[0-9]{6})((\/([A-Z0-9])*)*)))$'

    #t_SSMREF = r'[0-9]{6}'

    #t_SSMASM = r'(SSM|ASM)'

    #t_SSMTIME = r'(LT|UTC)'

    #def t_SSMTYPE(t):
        #r'(NEW|TIM|RPL|CNL|EQT|CON)'
        #global mtype
        #mtype = str(t.value)
        #return t

    #t_XASM = r'XASM'

    #t_FLTNUM = r'([A-Z]{2})([0-9]{3,4})'

    #t_DATE = r'[0123][0-9][A-Z]{3}[0-9]{2}'

    #t_NUMBER = r'[1-7]{1,7}'

    #t_ITEMDATA = r'[0-9]{1,3}\/[A-Z1-9]*'

    #def t_legs_ITEM(t):
        #r'[A-Z]{6}'
        #return t

    #def t_legs_ITENARY(t):
        #r'[A-Z]{3}[0-9]{4}'
        #return t

    #def t_legs_ITEMDATA(t):
        #r'[1-9][0-9]{2,3}\/[A-Z1-9]*'
        #return t

    ##t_FLIGHTINFO = r'(([A-Z]([A-Z]{1,2})([0-9]{1,4}))|([A-Z]([A-Z]{1,2})([0-9]{1,4})(\ [1-9]\/[A-Z]{2,3})*)|([1-9]\/[A-Z]{2,3}(\ [1-9]\/[A-Z]{2,3})*))'

    #def t_error(t):
        #raise TypeError("Unknown text '%s'" % (t.value,))

    ## Build the lexer from my environment and return it
    #return lex.lex()


def usage():
    print("Help!")
    sys.exit(1)


# Pythonic entry point
def main(argv):

    fname = None

    if len(argv) < 1:
        usage()

    for opt in argv:
        if opt == '-h' or opt == '--help':
            usage()
        elif opt == '-v':
            set_verbose(1)
        elif opt == '-V':
            set_verbose(2)
        #elif opt == '-I' or opt == '--input':
            #fname = str(arg)
        else:
            fname = str(opt)
            print("read '%s'" % fname)

    if fname is None or len(fname)==0:
        print("No input file specified")
        return 1

    print("read '%s'" % fname)

    if fname == "-":
        message = sys.stdin.read()
    else:
        f = open(fname)
        message = f.read()
        f.close()

    print("go")
    lex.lex()

    lex.input(message)

    for tok in iter(lex.token, None):
        print(repr(tok.type), end=' ')
        print(repr(tok.value))

    #for tok in iter(m.token, None):
        #print repr(tok.type), repr(tok.value)

    print("done")

    return 0


# Entry point
if __name__ == "__main__":
    rv = main(sys.argv[1:])
    sys.exit(rv)

