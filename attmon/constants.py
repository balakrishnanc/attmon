#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# constants.py
# Created by Balakrishnan Chandrasekaran on 2017-06-23 02:37 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

"""
constants.py
Frequently used constants.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>'
__version__ = '1.0'
__license__ = 'MIT'


import re


COLON = u':'
COMMA = u','
NEWLINE = u'\n'
TAB = u'\t'

# Precision (in terms of number of decimal places)
#  for RTT inflation computations.
PREC = 4

# Regular expressions to detect the beginning and ending of a table.
TAB_BEG_PAT = re.compile(r'<\s*table.*?>', re.IGNORECASE)
TAB_END_PAT = re.compile(r'<\s*/\s*table.*?>', re.IGNORECASE)

# Regular expressions to detect the beginning and ending of a table rows.
ROW_BEG_PAT = re.compile(r'<TR>')
ROW_END_PAT = re.compile(r'.*?</TR>.*?')

NO_VAL = u'&nbsp;'
NO_RTT = u'0'
# Regular expressions to parse the table data.
TD_VAL_PAT = re.compile(r'<TD .*?>' +
                        r'(?:<FONT.*?>(.*?)</FONT>|'
                        r'(' + NO_VAL + r'))</TD>')

# String used to identify the start of the table of values.
DATA_BEG_PAT = re.compile(r'<TD.*?>.*?CITY\s+PAIRS.*?</TD>')

# City abbreviations to city codes.
CTABBRV_CTCODE = {
    u'ATL' : u'US-GA-ATLANTA',
    u'AUS' : u'US-TX-AUSTIN',
    u'CAM' : u'US-MA-CAMBRIDGE',
    u'CHI' : u'US-IL-CHICAGO',
    u'CLE' : u'US-IL-CLEVELAND',
    u'DAL' : u'US-TX-DALLAS',
    u'DEN' : u'US-CO-DENVER',
    u'DET' : u'US-MI-DETROIT',
    u'HOU' : u'US-TX-HOUSTON',
    u'IND' : u'US-IN-INDIANAPOLIS',
    u'KAN' : u'US-KS-KANSASCITY',
    u'LA'  : u'US-CA-LOSANGELES',
    u'MAD' : u'US-WI-MADISON',
    u'NAS' : u'US-TN-NASHVILLE',
    u'NO'  : u'US-LA-NEWORLEANS',
    u'NY'  : u'US-NY-NEWYORK',
    u'ORL' : u'US-FL-ORLANDO',
    u'PA'  : u'US-PA-PHILADELPHIA',
    u'PHX' : u'US-AZ-PHOENIX',
    u'SA'  : u'US-TX-SANANTONIO',
    u'SD'  : u'US-CA-SANDIEGO',
    u'SF'  : u'US-CA-SANFRANCISCO',
    u'STL' : u'US-MO-STLOUIS',
    u'SEA' : u'US-WA-SEATTLE',
    u'WAS' : u'US-DC-WASHINGTON'
}

# City name to city codes.
CTNAME_CTCODE = {
    u'AUSTIN'        : u'US-TX-AUSTIN',
    u'CAMBRIDGE'     : u'US-MA-CAMBRIDGE',
    u'CHICAGO'       : u'US-IL-CHICAGO',
    u'CLEVELAND'     : u'US-IL-CLEVELAND',
    u'DALLAS'        : u'US-TX-DALLAS',
    u'DENVER'        : u'US-CO-DENVER',
    u'DETROIT'       : u'US-MI-DETROIT',
    u'HOUSTON'       : u'US-TX-HOUSTON',
    u'INDIANAPOLIS'  : u'US-IN-INDIANAPOLIS',
    u'KANSAS CITY'   : u'US-KS-KANSASCITY',
    u'LOS ANGELES'   : u'US-CA-LOSANGELES',
    u'MADISON'       : u'US-WI-MADISON',
    u'NASHVILLE'     : u'US-TN-NASHVILLE',
    u'NEW ORLEANS'   : u'US-LA-NEWORLEANS',
    u'NEW YORK'      : u'US-NY-NEWYORK',
    u'ORLANDO'       : u'US-FL-ORLANDO',
    u'PHILADELPHIA'  : u'US-PA-PHILADELPHIA',
    u'PHOENIX'       : u'US-AZ-PHOENIX',
    u'SAN ANTONIO'   : u'US-TX-SANANTONIO',
    u'SAN DIEGO'     : u'US-CA-SANDIEGO',
    u'SAN FRANCISCO' : u'US-CA-SANFRANCISCO',
    u'ST. LOUIS'     : u'US-MO-STLOUIS',
    u'SEATTLE'       : u'US-WA-SEATTLE',
    u'WASHINGTON'    : u'US-DC-WASHINGTON'
}
