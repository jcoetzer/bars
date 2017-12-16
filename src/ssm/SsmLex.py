# @file SsmLex.py

import ply.lex as lex

states = (
    ('equip','inclusive'),
    ('flight','inclusive'),
    ('legs','inclusive'),
    ('periods','inclusive'),
    ('classes','exclusive')
)

tokens = (
    'SPACE',
    'EOL',
    'DOT',
    'SLASH',
    'SSMQK',
    'ADRES',
    #'SSMSENDER',
    'SSMREF',
    'MTIME',
    'MTYPE',
    'ACTION',
    'XASM',
    'FLTNUM',
    'DATE',
    'NUMBER',
    'LETTER',
    'PAXBOOK',
    'SSMJ',
    'AIRCRFT',
    'CLASS',
    'VVM',
    'TAIL',
    'ITEM',
    'ITEMDATA',
    'ITENARY',
    'DATA'
    #'FLIGHTINFO'
)

mtype = None
verbose = 0

t_SPACE = r'[ ]'

t_EOL = r'[\n]'

t_DOT = r'[\.]'

t_SLASH = r'[\/]'

def t_SSMJ(t):
    r'[J][\ ]'
    t.lexer.begin('equip')
    return t

def t_equip_EOL(t):
    r'[\n]'
    t.lexer.begin('legs')
    return t

def t_equip_AIRCRFT(t):
    r'[0-9][A-Z0-9]{2}'
    return t

def t_DATA(t):
    r'[\/][A-Z1-9]*'
    return t

t_SSMQK = r'QK'

t_ADRES = r'[A-Z][A-Z0-9]{5,6}'

#t_SSMSENDER = r'\.[A-Z][A-Z0-9]{6}[\ ][0-9]{6}'
#t_SSMSENDER = r'((\.[A-Z]([A-Z0-9]{6})((\ ([0-9]{6}))*))|([A-Z]([A-Z]{6})\ ([A-Z]{2}\/[0-9]{6})((\/([A-Z0-9])*)*)))$'

t_SSMREF = r'[0-9]{6}'

t_MTYPE = r'(SSM|ASM)'

t_MTIME = r'(LT|UTC)'

# ACTION
def t_ACTION(t):
    r'(NEW|TIM|RPL|CNL|EQT|CON)'
    global mtype
    mtype = str(t.value)
    t.lexer.begin('flight')
    return t

t_XASM = r'XASM'

t_flight_FLTNUM = r'([A-Z]{2})([0-9]{3,4})'

def t_flight_EOL(t):
    r'\n'
    t.lexer.begin('periods')
    return t

def t_periods_DATE(t):
    r'[0123](JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[0-9]{2}'
    return t

def t_periods_FREQ(t):
    r'[1-7]{1,7}'
    return t

def t_periods_EOL(t):
    r'[\n]'
    t.lexer.begin('equip')
    return t

t_equip_LETTER =  r'[A-Z]'

t_equip_PAXBOOK = r'[X]{2}'

def t_equip_NUMBER(t):
    r'[0-9]{2}'
    return t

def t_equip_TAIL(t):
    r'ZS[A-Z]{3}'
    return t

def t_equip_DOT(t):
    r'[\.]'
    t.lexer.begin('classes')
    return t

def t_classes_CLASS(t):
    r'[A-Z][0-9]{1,3}'
    return t

def t_classes_end(t):
    r'VVM|\n'
    t.lexer.begin('equip')

t_ITEMDATA = r'[0-9]{1,3}\/[A-Z1-9]*'

def t_legs_ITEM(t):
    r'[A-Z]{6}'
    return t

def t_legs_ITENARY(t):
    r'[A-Z]{3}[0-9]{4}'
    return t

def t_legs_ITEMDATA(t):
    r'[1-9][0-9]{2,3}\/[A-Z1-9]*'
    return t

#t_FLIGHTINFO = r'(([A-Z]([A-Z]{1,2})([0-9]{1,4}))|([A-Z]([A-Z]{1,2})([0-9]{1,4})(\ [1-9]\/[A-Z]{2,3})*)|([1-9]\/[A-Z]{2,3}(\ [1-9]\/[A-Z]{2,3})*))'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

# Build the lexer from this environment
lex.lex()
