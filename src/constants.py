"""
.. Copyright (c) 2015 Marshall Farrier, Robert Rodrigues, Mark Scappini
   license http://opensource.org/licenses/MIT

Constants
=========
"""

# Configuration
SERVICE_NAME = 'quotepuller'
CONFIGFILE = '/etc/quichean/{}.cfg'.format(SERVICE_NAME)
CFGSECTION_MAIN = 'Main'

# database
DB = 'optionsMkt'
DB_TEST = 'optionsTst'

# collections
EQUITIES = 'equities'
QUOTES = 'quotes'
FIELDNAMES = ('Quote_Time', 'Underlying', 'Expiry', 'Opt_Type', 'Strike', 'Opt_Symbol',\
        'Last', 'Bid', 'Ask', 'Vol', 'Open_Int',)
INTFIELDS = ('Vol', 'Open_Int',)
FLOATFIELDS = ('Strike', 'Last', 'Bid', 'Ask',)
DATEFIELDS = ('Quote_Time', 'Expiry',)
STRFIELDS = ('Underlying', 'Opt_Type', 'Opt_Symbol',)

# retry parameters
RETRYSECS_QUOTES = 10 * 60
RETRYSECS_QUOTES_TST = 60
RETRYSECS_DBCONNECT = 5. * 60.
N_DBRETRIES = 2
