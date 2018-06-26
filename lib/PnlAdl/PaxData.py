"""
Passenger data.

@file PaxData.cpp
"""

from BarsLog import get_verbose, printlog


class PaxData(object):

    def __init__(self, pnladlrep=''):
        """Get this show on the road."""
        self.paxrep = pnladlrep

    def Clear(self):
        """Constructor."""
        printlog(2, "\tReset pax data")
        self.paxno = 0
        self.paxcount = ''
        self.paxname = ''
        self.grpname = ''
        self.locator = ''
        self.etickt = ''
        self.eticktinf = ''
        self.etlp = ''
        self.etlpinf = ''
        self.chekin = ''
        self.inft = ''
        self.marketflt = ''
        self.incomingflt = ''
        self.outgoingflt = ''
        self.pnladlerr = 0
        self.paxrec = 'FLY'

    def Add(self, pdata, aCodeShare):
        """Add another one."""
        if len(pdata) == 0:
            return 0
        self.Requests = ''
        self.codeShare = aCodeShare
        printlog(1, "pax [%s]" % pdata)
        elements = pdata.split('.')
        self.CheckName(elements[0])
        i = 1
        while i < len(elements):
            self.CheckElement(elements[i])
            i += 1
        return 0

    def CheckName(self, ndata):
        """Check passenger name."""
        nel = ndata.split('-')
        found = nel[0].find_first_not_of("1234567890")

        if found is None:
            print("Invalid name '%s'", nel[0])
            return 1

        self.paxcount = nel[0].substr(0, found)
        printlog(1, "\tcount '%s'" % self.paxcount)

        self.paxname = nel[0][found:].rstrip()
        printlog(1, "\tname '%s'" % self.paxname)

        if (len(nel) > 1 and len(nel[1]) > 0 and nel[1][1] != '/'):
            self.grpname = nel[1].strip()
            printlog(1, "\tgroup '%s'" % self.grpname)
        return 0

    def CheckElement(self, edata):
        """Check marketing element."""
        indata = ''
        if (edata[0:1] == "L"):
            locator = edata.substr(2).strip()
            printlog(1, "\tlocator '%s'" % locator)
        elif (edata[0] == "R"):
            self.CheckRemark(edata[2])
        elif (edata.substr[0] == "M"):
            marketflt = edata.substr(2).strip()
            if (marketflt.length() <= 9):
                print("Marketing element '%s' not valid" % marketflt)
                self.pnladlerr += 1
            else:
                indata = marketflt.substr(0, marketflt.length()-9)
                printlog(1, "\tmarketing '%s' for %s" % (marketflt, indata))
                if len(self.codeShare) == 0:
                    print("Marketing element for non-codeshare flight")
                    self.pnladlerr += 1
                elif (self.codeShare != indata):
                    print("Codeshare flight number should be '%s' and not '%s'"
                          % (self.codeShare, indata))
                    self.pnladlerr += 1
        elif (edata[0] == "I"):
            incomingflt = edata.substr(2).rstrip()
            printlog(1, "\tincoming flight %s" % incomingflt)
        elif (edata[0] == "O"):
            outgoingflt = edata[2:].rstrip()
            printlog(1, "\toutgoing flight %s" % outgoingflt)
        else:
            printlog(1, "\tother '%s'" % edata)
        return 0

    def AddRemark(self, rdata):
        """Add remark text."""
        self.Requests.append(rdata)

    def CheckRemark(self, rdata):
        """Check remark text."""
        self.Requests.append(rdata)
        if (rdata[0:4] == "TKNE"):
            if (rdata.length() < 9):
                self.pnladlerr += 1
                self.paxrep += "Invalid e-ticket "
                self.paxrep += rdata
                self.paxrep += ""
                print("Invalid e-ticket %s" % rdata)
            elif (rdata.substr(9, 3) == "INF"):
                if len(self.eticktinf):
                    self.pnladlerr += 1
                    print("Duplicate infant e-ticket")
                eticktinf = rdata[9:].rstrip()
                printlog(1, "\tinfant e-ticket '%s'", eticktinf)
            elif (rdata.substr(5, 3) != "HK1"):
                self.paxrep += "Invalid e-ticket action code "
                self.paxrep += rdata
                self.paxrep += ""
                print("Action code and number is '%s' and not HK1"
                      % rdata[5:8])
                self.pnladlerr += 1
            else:
                if len(self.etickt) > 0:
                    self.pnladlerr += 1
                    print("Duplicate e-ticket '%s'" % self.etickt)
                self.etickt = rdata[9:].rstrip()
                printlog(1, "\te-ticket '%s'", self.etickt)
        elif (rdata[0:4] == "ETLP"):
            if (rdata.length() < 9):
                self.pnladlerr += 1
                self.paxrep += "Invalid ticket "
                self.paxrep += rdata
                self.paxrep += ""
                print("Invalid ticket %s", rdata)
            elif (rdata.substr(9, 3) == "INF"):
                if len(self.etlpinf) > 0:
                    self.pnladlerr += 1
                    print("Duplicate infant ticket")
                self.etlpinf = rdata[9:].rstrip()
                printlog(1, "\tinfant ticket '%s'", self.etlpinf)
            else:
                if len(self.etlp) > 0:
                    self.pnladlerr += 1
                    print("Duplicate ticket")
                self.etlp = rdata[9:].rstrip()
                printlog(1, "\tticket '%s'", self.etlp)
        elif (rdata[0:4] == "CKIN"):
            self.chekin = rdata[5:].rstrip()
            printlog(1, "\tcheckin '%s'", self.chekin)
        elif (rdata[0:4] == "INFT"):
            self.inft = rdata[5:].rstrip()
            printlog(1, "\tinfant '%s'", self.inft)
        else:
            printlog(1, "\tremark '%s'", self.rdata)
        return 0

    def Check(self):
        """
        Final check for errors.

        @return number of errors found
        """
        if (len(self.inft) and len(self.eticktinf) == 0 and len(self.etlpinf)):

            self.paxrep += "No ticket number for infant"
            if len(self.etickt) == 0:
                print("No e-ticket number for infant")
            else:
                print("No ticket number for infant")
            self.pnladlerr += 1
        if len(self.locator) == 0:
            self.paxrep += "No locator"
            print("No locator for '%s'" % self.paxname)
            self.pnladlerr += 1
        return self.pnladlerr

    def PrintRequests(self):
        """Print out requests."""
        for pit in self.Requests:
            print(".R/%s " % pit)
        return len(self.Requests)

    def GetRequestCount(self):
        """Number of requests."""
        if (get_verbose() >= 2):
            for it in self.Requests:
                print("\tpax SSR: %s" % it)
        return len(self.Requests)