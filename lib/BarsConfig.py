"""
BARS configuration file.
"""

import configparser


class BarsConfig(object):
    """
    BARS configuration.
    """
    DbName = 'barsdb'
    dbuser = 'postgres'
    dbhost = 'localhost'
    AirlineNo = 0
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
    FareBasisCode = 'YZZOW'
    BookCategory = 'S'     # or G for groups
    Address = 'SWIZZ1G'
    Sender = 'JNB0AZZ'
    TimeMode = 'LT'
    DialCode = '+27'
    PaymentFail = 0

    def __init__(self, cfgfile):
        """Initialize this thing."""

        config = configparser.ConfigParser()
        config.readfp(open(cfgfile))

        self.dbname = config.get('Database', 'dbname')
        self.dbuser = config.get('Database', 'dbuser')
        self.dbhost = config.get('Database', 'dbhost')
        self.AirlineNo = int(config.get('Airline', 'AirlineNo'))
        self.OnwReturnIndicator = config.get('Airline', 'OnwReturnIndicator')
        self.AuthorityLevel = int(config.get('Airline', 'AuthorityLevel'))
        self.FareCategory = config.get('Airline', 'FareCategory')
        self.CompanyCode = config.get('Airline', 'CompanyCode')
        self.OriginAddress = config.get('Airline', 'OriginAddress')
        self.OriginBranchCode = config.get('Airline', 'OriginBranchCode')
        self.AgencyCode = config.get('Airline', 'AgencyCode')
        self.SellingClasses = config.get('Airline', 'SellingClasses')
        self.PaxCode = config.get('Airline', 'PaxCode')
        self.FareBasisCode = config.get('Airline', 'FareBasisCode')
        self.BookCategory = config.get('Airline', 'BookCategory')
        self.User = config.get('Users', 'User')
        self.Group = config.get('Users', 'Group')
        self.Currency = config.get('Country', 'Currency')
        self.DialCode = config.get('Country', 'DialCode')

        self.Address = config.get('Tty', 'Sender')
        self.Sender = config.get('Tty', 'Sender')

        self.PaymentFail = int(config.get('Payment', 'PaymentFail'))
