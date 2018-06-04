import ConfigParser

class BarsConfig(object):

    DbName = 'barsdb'
    dbuser = 'postgres'
    dbhost = 'localhost'
    OnwReturnIndicator = 'R'
    AuthorityLevel = 100
    FareCategory = 'ZZOW'
    CompanyCode = 'ZZ'
    SellingClass = 'Y'
    OriginAddress = 'HDQOTZZ'
    OriginBranchCode = 'SNAFU'
    AgencyCode = 'TARFU'
    User = 'JOHN'
    Group = 'BANANA'
    PaxCode = 'ADULT'
    Currency = 'ZAR'
    FareCode = 'XZZOW'
    BookCategory = 'S'     # or G for groups

    def __init__(self, cfgfile):
        """Initialize this thing."""

        config = ConfigParser.ConfigParser()
        config.readfp(open(cfgfile))

        self.dbname = config.get('Database', 'dbname')
        self.dbuser = config.get('Database', 'dbuser')
        self.dbhost = config.get('Database', 'dbhost')
        self.OnwReturnIndicator = config.get('Airline', 'OnwReturnIndicator')
        self.AuthorityLevel = int(config.get('Airline', 'AuthorityLevel'))
        self.FareCategory = config.get('Airline', 'FareCategory')
        self.CompanyCode = config.get('Airline', 'CompanyCode')
        self.OriginAddress = config.get('Airline', 'OriginAddress')
        self.OriginBranchCode = config.get('Airline', 'OriginBranchCode')
        self.AgencyCode = config.get('Airline', 'AgencyCode')
        self.SellingClasses = config.get('Airline', 'SellingClasses')
        self.PaxCode = config.get('Airline', 'PaxCode')
        self.FareCode = config.get('Airline', 'FareCode')
        self.BookCategory = config.get('Airline', 'BookCategory')
        self.User = config.get('Users', 'User')
        self.Group = config.get('Users', 'Group')
        self.Currency = config.get('Country', 'Currency')

