# @file SsmLex.py
"""
Lex and flex away.
"""
import ply.lex as lex
from BarsLog import printlog, set_verbose

states = (
    ('equip','exclusive'),
    ('flight','exclusive'),
    ('legs','exclusive'),
    ('periods','exclusive'),
    ('segments','exclusive'),
    ('classes','exclusive')
)

tokens = (
    'SPACE',
    'EOL',
    'DOT',
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
    'FREQ',
    #'NUMBER',
    'PAXBOOK',
    'STYPE',
    'AIRCRFT',
    'CLASS',
    'VVM',
    'TAIL',
    'ITEM',
    'ITEMDATA',
    'LEGSTN',
    'SEGMENT',
    'DATA'
    #'FLIGHTINFO'
)

mtype = None
verbose = 0

def t_SPACE(t):
    r'[ ]'
    pass

def t_EOL(t):
    r'[\n|\003]'
    printlog(2, ">>>EOL ")
    return t

t_DOT = r'[\.]'

def t_DATA(t):
    r'[\/][A-Z1-9]*'
    return t

def t_SSMQK(t):
    r'QK'
    pass

# ADRES
def t_ADRES(t):
    r'[A-Z][A-Z0-9]{5,6}'
    printlog(2, ">>>ADRES %s" % t.value)
    return t


t_SSMREF = r'[0-9]{6}'

t_MTYPE = r'(SSM|ASM)'

t_MTIME = r'(LT|UTC)'

# ACTION
def t_ACTION(t):
    r'(NEW|TIM|RPL|CNL|EQT|CON)'
    global mtype
    mtype = str(t.value)
    printlog(2, ">>>ACTION %s" % mtype)
    tok = t.lexer.token()             # Get the next token
    printlog(2, ">>> State flight")
    t.lexer.begin('flight')
    return t

t_XASM = r'XASM'

# --- flight ---

def t_flight_error(t):
    raise TypeError("Unknown flight text '%s'" % (t.value,))

def t_flight_FLTNUM(t):
    r'([A-Z]{2})([0-9]{3,4})'
    printlog(2, ">>>FLTNUM %s" % t.value)
    return t

def t_flight_SPACE(t):
    r'[ ]'
    pass

def t_flight_ADRES(t):
    r'([A-Z]{2})([0-9]{3,4})'
    printlog(2, ">>>ADRES %s" % t.value)
    return t

def t_flight_ITEMDATA(t):
    r'[1-9]\/[A-Z1-9]*'
    printlog(2, ">>>ITEMDATA %s" % t.value)
    return t

def t_flight_EOL(t):
    r'[\n|\003]'
    printlog(2, ">>>EOL")
    printlog(2, ">>> State periods")
    t.lexer.begin('periods')
    return t

# --- periods ---

def t_periods_error(t):
    raise TypeError("Unknown periods text '%s'" % (t.value,))

def t_periods_DATE(t):
    r'[0123][0-9](JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[0-9]{2}'
    printlog(2, ">>>DATE %s" % t.value)
    return t

def t_periods_SPACE(t):
    r'[ ]'
    pass

def t_periods_FREQ(t):
    r'[1-7]{1,7}'
    printlog(2, ">>>FREQ %s" % t.value)
    return t

def t_periods_EOL(t):
    r'[\n|\003]'
    printlog(2, ">>>EOL")
    #tok = t.lexer.token()             # Get the next token
    printlog(2, ">>> State equip")
    t.lexer.begin('equip')
    return t

# --- equip ---

def t_equip_error(t):
    raise TypeError("Unknown equip text '%s'" % (t.value,))

# STYPE
def t_equip_STYPE(t):
    r'[A-Z][ ]'
    printlog(2, ">>>STYPE %s" % t.value)
    return t

def t_equip_SPACE(t):
    r'[ ]'
    pass

def t_equip_PAXBOOK(t):
    r'[X]{2}'
    printlog(2, ">>>PAXBOOK %s" % t.value)
    return t


# AIRCRFT
def t_equip_AIRCRFT(t):
    r'[0-9][A-Z0-9]{2}'
    printlog(2, ">>>AIRCRFT %s" % t.value)
    return t

def t_equip_TAIL(t):
    r'ZS[A-Z]{3}'
    printlog(2, ">>>TAIL %s" % t.value)
    return t

def t_equip_DOT(t):
    r'[\.]'
    printlog(2, ">>>DOT")
    t.lexer.begin('classes')
    printlog(2, ">>> State classes")
    return t

def t_equip_EOL(t):
    r'[\n|\003]'
    printlog(2, ">>>EOL")
    printlog(2, ">>> State legs")
    t.lexer.begin('legs')
    return t

# --- classes ---

def t_classes_error(t):
    raise TypeError("Unknown classes text '%s'" % (t.value,))

def t_classes_CLASS(t):
    r'[A-Z][0-9]{1,3}'
    printlog(2, ">>>CLASS %s" % t.value)
    return t

def t_classes_SPACE(t):
    r'\ '
    printlog(2, ">>> State equip")
    t.lexer.begin('equip')
    pass

def t_classes_end(t):
    r'VVM|\n'
    printlog(2, ">>> State equip")
    t.lexer.begin('equip')

# --- legs ---

def t_legs_error(t):
    raise TypeError("Unknown legs text '%s'" % (t.value,))

def t_legs_ITEM(t):
    r'[A-Z]{6}'
    printlog(2, ">>>ITEM %s" % t.value)
    return t

def t_legs_SPACE(t):
    r'[ ]'
    pass

def t_legs_LEGSTN(t):
    r'[A-Z]{3}[0-9]{4}'
    printlog(2, ">>>LEGSTN %s" % t.value)
    return t

def t_legs_ITEMDATA(t):
    r'[1-9][0-9]{2,3}\/[A-Z1-9]*'
    printlog(2, ">>>ITEMDATA %s" % t.value)
    return t

def t_legs_FREQ(t):
    r'[1-7]{1,7}'
    printlog(2, ">>>FREQ %s" % t.value)
    #tok = t.lexer.token()             # Get the next token
    printlog(2, ">>> State segments")
    t.lexer.begin('segments')
    return t

def t_legs_EOL(t):
    r'[\n|\003]'
    printlog(2, ">>>EOL")
    printlog(2, ">>> State segments")
    t.lexer.begin('segments')
    return t

# --- segments ---

def t_segments_error(t):
    edata = str(t.value,)
    if len(edata) == 1:
        printlog(2, "Weird character %d" % ord(edata[0]))
    else:
        printlog(2, "Unknown segments text %d bytes" % (len(edata)))
        raise TypeError("Unknown segments text '%s'" % edata)

def t_segments_SEGMENT(t):
    '[A-Z]{6}'
    printlog(2, ">>>SEGMENT %s" % t.value)
    return t

def t_segments_ITEMDATA(t):
    r'[1-9][0-9]{0,2}\/[A-Z0-9]*'
    printlog(2, ">>>ITEMDATA %s" % t.value)
    return t

def t_segments_SPACE(t):
    r'[ ]'
    pass

def t_segments_EOL(t):
    r'[\n|\003]'
    printlog(2, ">>>EOL")
    return t

#t_FLIGHTINFO = r'(([A-Z]([A-Z]{1,2})([0-9]{1,4}))|([A-Z]([A-Z]{1,2})([0-9]{1,4})(\ [1-9]\/[A-Z]{2,3})*)|([1-9]\/[A-Z]{2,3}(\ [1-9]\/[A-Z]{2,3})*))'

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

# Build the lexer from this environment
# set_verbose(2)
lex.lex()
