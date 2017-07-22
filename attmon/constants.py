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
NO_LOSS = u'-1'
# Regular expressions to parse the table data.
TD_VAL_PAT = re.compile(r'<TD .*?>' +
                        r'(?:<FONT.*?>(.*?)</FONT>|'
                        r'(' + NO_VAL + r'))</TD>')

# String used to identify the start of the table of values.
DATA_BEG_PAT = re.compile(r'<TD.*?>.*?CITY\s+PAIRS.*?</TD>')
