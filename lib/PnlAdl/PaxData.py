"""
Passenger data.

@file PaxData.cpp
"""



class PaxData(object):

    def __init__(self, pnladlrep=''):
        """Get this show on the road."""
        self.paxrep = pnladlrep

    def Clear():
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

        self.Requests = ''

        if (! pdata.length())
            return 0

        codeShare = aCodeShare

        printlog(1, "pax [%s]", pdata)

        vector<string> elements = split(pdata, '.')

        CheckName(elements[0])

        i = 1
        while i < len(elements):

            CheckElement(elements[i])
            i += 1


        return 0


    def CheckName(self, ndata):

        nel = ndata.split('-')

        found = nel[0].find_first_not_of("1234567890")

        if found is None:

            printf("Invalid name '%s'", nel[0])
            return 1

        paxcount = nel[0].substr(0, found)
        printlog(1, "\tcount '%s'", paxcount)

        paxname = nel[0].substr(found)
        rtrim(paxname)
        printlog(1, "\tname '%s'" % paxname)

        if (len(nel) > 1 and  len(nel[1]) > 0 and nel[1][1] != '/'):

            grpname = nel[1]
            rtrim(grpname)
            printlog(1, "\tgroup '%s'" % grpname)


        return 0


    def CheckElement(self, edata)

        indata = ''

        if (edata.substr(0, 1) == "L")

            locator = edata.substr(2)
            rtrim(locator)
            printlog(1, "\tlocator '%s'", locator)

        elif (edata.substr(0, 1) == "R")

            CheckRemark(edata.substr(2))

        elif (edata.substr(0, 1) == "M")

            marketflt = edata.substr(2)
            rtrim(marketflt)
            if (marketflt.length() <= 9)

                printf("Marketing element '%s' not valid", marketflt)
                ++pnladlerr

            else

                indata = marketflt.substr(0, marketflt.length()-9)
                printlog(1, "\tmarketing '%s' for %s", marketflt, indata)
                if (! codeShare.length())

                    printf("Marketing element for non-codeshare flight")
                    ++pnladlerr

                elif (codeShare != indata)

                    printf("Codeshare flight number should be '%s' and not '%s'", codeShare, indata)
                    ++pnladlerr



        elif (edata.substr(0, 1) == "I")

            incomingflt = edata.substr(2)
            rtrim(incomingflt)
            printlog(1, "\tincoming flight %s", incomingflt)

        elif (edata.substr(0, 1) == "O")

            outgoingflt = edata.substr(2)
            rtrim(outgoingflt)
            printlog(1, "\toutgoing flight %s", outgoingflt)

        else
            printlog(1, "\tother '%s'", edata)
        return 0


    def AddRemark(self, rdata)
        """Add remark text."""
        self.Requests.append(rdata)

    def CheckRemark(self, rdata):

        self.Requests.append(rdata)
        if (rdata.substr(0, 4) == "TKNE")

            if (rdata.length() < 9)

                ++pnladlerr
                paxrep += "Invalid e-ticket "
                paxrep += rdata
                paxrep += ""
                printf("Invalid e-ticket %s", rdata)

            elif (rdata.substr(9, 3) == "INF")

                if (eticktinf.length())

                    ++pnladlerr
                    printf("Duplicate infant e-ticket")

                eticktinf = rdata.substr(9)
                rtrim(eticktinf)
                printlog(1, "\tinfant e-ticket '%s'", eticktinf)

            elif (rdata.substr(5, 3) != "HK1")

                paxrep += "Invalid e-ticket action code "
                paxrep += rdata
                paxrep += ""
                printf("Action code and number is '%s' and not HK1", rdata.substr(5, 3))
                ++pnladlerr

            else

                if (etickt.length())

                    ++pnladlerr
                    printf("Duplicate e-ticket '%s'", etickt)

                etickt = rdata.substr(9)
                rtrim(etickt)
                printlog(1, "\te-ticket '%s'", etickt)


        elif (rdata.substr(0, 4) == "ETLP")

            if (rdata.length() < 9)

                ++pnladlerr
                paxrep += "Invalid ticket "
                paxrep += rdata
                paxrep += ""
                printf("Invalid ticket %s", rdata)

            elif (rdata.substr(9, 3) == "INF")

                if (etlpinf.length())

                    ++pnladlerr
                    printf("Duplicate infant ticket")

                etlpinf = rdata.substr(9)
                rtrim(etlpinf)
                printlog(1, "\tinfant ticket '%s'", etlpinf)

            else

                if (etlp.length())

                    ++pnladlerr
                    printf("Duplicate ticket")

                etlp = rdata.substr(9)
                rtrim(etlp)
                printlog(1, "\tticket '%s'", etlp)


        elif (rdata.substr(0, 4) == "CKIN")

            chekin = rdata.substr(5)
            rtrim(chekin)
            printlog(1, "\tcheckin '%s'", chekin)

        elif (rdata.substr(0, 4) == "INFT")

            inft = rdata.substr(5)
            rtrim(inft)
            printlog(1, "\tinfant '%s'", inft)

        else

            printlog(1, "\tremark '%s'", rdata)


        return 0


    def Check()
        """
        Final check for errors.

        @return number of errors found
        """
        if (len(self.inft) and len(self.eticktinf) == 0 and len(self.etlpinf)):

            paxrep += "No ticket number for infant"
            if len(etickt) > 0:
                printf("No e-ticket number for infant")
            else:
                printf("No ticket number for infant")
            ++pnladlerr

        if (0==locator.size())

            paxrep += "No locator"
            printf("No locator for '%s'", paxname)
            ++pnladlerr


        return pnladlerr


    def PrintRequests(self):

        for pit in self.Requests:
            printf(".R/%s ", pit->c_str())
        return len(self.Requests)


    def GetRequestCount(self):

        if (verbose>=2)
            for (vector<string >::iterator it = Requests.begin() it != Requests.end() it++)
                printf("\tpax SSR: %s", it->c_str())
        return Requests.size()


