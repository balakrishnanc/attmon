#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# rttmon.py
# Created by Balakrishnan Chandrasekaran on 2017-06-23 02:23 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

"""
rttmon.py
Fetch network latency values reported by AT&T.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>'
__version__ = '1.0'
__license__ = 'MIT'


from constants import *
import io


def proc_row(row):
    """Process data in the current row.
    """
    if len(row) == 1:
        return (None, None, row[-1])
    return (row[0], row[1:-1], row[-1])


def parse_page(page):
    """Parse Web page and report the latency matrix on the page.
    """
    # Flag indicating when to begin scanning.
    scan = False
    # Flag indicating when to begin processing table data.
    proc = False
    # Flag indicating the ID of the column we are parsing within a row.
    col_num = 0

    rtt_matrix = {}
    # Column headers.
    col_hdrs = []
    # Current row.
    curr_row = []

    for line in (line.strip() for line in page.split(NEWLINE) if line):
        if not scan and TAB_BEG_PAT.match(line):
            scan = True
        elif not scan:
            continue

        if not proc and DATA_BEG_PAT.match(line):
            proc = true
            continue
        elif not proc:
            continue

        if ROW_BEG_PAT.match(line) and curr_row:
                raise ValueError('Failed to detect a closing row tag!')

        # Table data.
        td_val = TD_VAL_PAT.match(line)
        if td_val:
            # Check for 'blank' cells!
            val = td_val.group(1)
            if not val:
                if td_val.group(2).strip() != NO_VAL:
                    raise ValueError('Unable to parse table data!')

                val = NO_RTT

            curr_row.append(val.strip())

        if ROW_END_PAT.match(line):
            src, rtts, hdr = proc_row(curr_row)

            if not src and not rtts:
                col_hdrs.append(CTABBRV_CTCODE[hdr.upper()])
            elif len(rtts) != len(col_hdrs):
                raise ValueError('Unknown data format!')
            else:
                cc = CTNAME_CTCODE[src.upper()]
                rtt_matrix[cc] = {dst:int(rtt)
                                  for dst,rtt in zip(col_hdrs, rtts)}
                col_hdrs.append(CTABBRV_CTCODE[hdr.upper()])

            curr_row = []


        if proc and TAB_END_PAT.match(line):
            break

    return rtt_matrix


def show_matrix(m):
    """Display cells of the matrix.
    """
    for r in sorted(m.keys()):
        for c in sorted(m[r].keys()):
            print("%20s %-20s %+2d" % (r, c, m[r][c]))
