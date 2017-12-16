# @file SsmData.py

# Set action
def set_action(atype):
    print "Action %s" % (atype)

# Set time zone
def set_time_zone(atz):
    print "Time zone %s" % (atz)

# Add flight number
def add_flight_number(afnum, airline):
    print "Flight %s" % (afnum)

#
def add_leg(depart, arrive, days):
    print " %s  %s  %s" % (depart, arrive, days)

# Add dates and frequencies
def add_dates_freq(sdate, edate, freq):
    print "Start %s end %s frequency %s" % (sdate, edate, freq)

# Add segment
def add_segment(dep, arr, acode, adata):
    print "Depart %s arrive %s aircraft %s data %s" % (dep, arr, acode, adata)

def add_segment3(dep, arr, acode, adata1, adata2, adata3):
    print "Depart %s arrive %s aircraft %s data %s %s %s" % (dep, arr, acode, adata1, adata2, adata3)

# Add configuration
def add_config(adata):
    print "Configuration %s" % (adata)

# Add equipment
def add_equipment(atype, abook, adata, atail):
    print "Type %s book %s data %s tail %s" % (atype, abook, adata, atail)
