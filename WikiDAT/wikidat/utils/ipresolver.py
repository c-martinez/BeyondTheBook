'''
Created on Jul 24, 2014

This package provides functionality for resolving originating country for a requested IP address.

@author: carlosm
'''

import ipaddress
import bisect
import os

def __load_data__():
    # Load data from __DBIP_FILE__
    # File __DBIP_FILE__ is a file with IP ranges downloaded from http://db-ip.com/db/
    # (Data downloaded 24 June 2014).
    data = []
    path = os.path.dirname(__file__)
    dbip = path + '/' + __DBIP_FILE__

    with open(dbip, 'r') as fin:
        for line in fin:
            line = line.strip()
            cols = line.split(',')
    
            fromIP_str = cols[0].strip('"')
            toIP_str = cols[1].strip('"')
            country = cols[2].strip('"')
    
            fromIP = ipaddress.ip_address(unicode(fromIP_str))
            toIP = ipaddress.ip_address(unicode(toIP_str))
    
            fromIP_int = int(fromIP)
            toIP_int = int(toIP)
    
            data.append((fromIP_int, toIP_int, country))
    
    lowerAdd = [ x[0] for x in data ]
    upperAdd  = [ x[1] for x in data ]
    country  = [ x[2] for x in data ]

    # PATCH replace GB's for UK's
    country = [ cc if cc!='GB' else 'UK' for cc in country ]
    
    return lowerAdd, upperAdd, country

def getCountryCode(ip_str):
    '''
    For a given ip address (as string), locate its country code.
    
    ip_str        Target IP address (as string)
    lowerAdd      List of lower ranges
    upperAdd      List of upper ranges
    countryCodes  Range country codes
    
    Return the target countr code (or NaN if not know.)
    '''
    try:
        ip = ipaddress.ip_address(unicode(ip_str))
    except:
        # Invalid IP
        return None
    ip_int = int(ip)

    idx = bisect.bisect_left(__UPPER_ADD__, ip_int)

    if __LOWER__ADD__[idx]<=ip_int and ip_int<=__UPPER_ADD__[idx]:
        return __COUNTRY__[idx]
    else:
        ip_t = str(ip_int)
        ip_l = str(__LOWER__ADD__[idx])
        ip_h = str(__UPPER_ADD__[idx])
        print 'Address ' + ip_t + ' is not in range [' + ip_l + ', ' +  ip_h + ']'
        return None

# Initialize module
__DBIP_FILE__ = 'dbip-country.csv'
__LOWER__ADD__, __UPPER_ADD__, __COUNTRY__ = __load_data__()

if __name__=='__main__':
    '''
    Test source country IP's from know locations.
    '''
    assert getCountryCode('145.100.61.14')=='NL' # Netherlands eScience center IP
    assert getCountryCode('144.173.6.146')=='UK' # U. Exeter IP
    assert getCountryCode('74.125.136.106')=='US' # www.google.com
    assert getCountryCode('148.243.168.33')=='MX' # www.eluniversal.com.mx
