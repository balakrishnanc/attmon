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


from . import constants as const
from . import stats
from . import utils
import io
import math


# Missing delay value.
NO_RTT_VAL = float(const.NO_RTT)


def proc_row(row):
    """Process data in the current row.
    """
    if len(row) == 1:
        return (None, None, row[-1])
    return (row[0], row[1:-1], row[-1])


def parse(page, city_data):
    """Parse Web page and report the latency matrix on the page.
    """
    # Mapping from abbreviations and city names to city codes.
    abbrvs, cnames = city_data
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

    for line in (line.strip() for line in page.split(const.NEWLINE) if line):
        if not scan and const.TAB_BEG_PAT.match(line):
            scan = True
        elif not scan:
            continue

        if not proc and const.DATA_BEG_PAT.match(line):
            proc = True
            continue
        elif not proc:
            continue

        if const.ROW_BEG_PAT.match(line) and curr_row:
                raise ValueError('Failed to detect a closing row tag!')

        # Table data.
        td_val = const.TD_VAL_PAT.match(line)
        if td_val:
            # Check for 'blank' cells!
            val = td_val.group(1)
            if not val:
                if td_val.group(2).strip() != const.NO_VAL:
                    raise ValueError('Unable to parse table data!')

                val = const.NO_RTT

            curr_row.append(val.strip())

        if const.ROW_END_PAT.match(line):
            src, rtts, hdr = proc_row(curr_row)

            if not src and not rtts:
                col_hdrs.append(abbrvs[hdr.upper()])
            elif len(rtts) != len(col_hdrs):
                raise ValueError('Unknown data format!')
            else:
                cc = cnames[src.upper()]
                rtt_matrix[cc] = {dst:int(rtt)
                                  for dst,rtt in zip(col_hdrs, rtts)}
                col_hdrs.append(abbrvs[hdr.upper()])

            curr_row = []


        if proc and const.TAB_END_PAT.match(line):
            break

    return rtt_matrix, stats.compute(rtt_matrix, NO_RTT_VAL)


def calc_dist(x, y):
    """Calculate the navigational distance between any two
    physical points on the surface of Earth using the Haversine
    formula(http://www.movable-type.co.uk/scripts/latlong.html).
    """
    latx, lonx = x
    laty, lony = y
    # mean Earth radius
    R = 6371.0
    dlat = math.radians(latx - laty)
    dlon = math.radians(lonx - lony)
    a = ((math.sin(dlat / 2) * math.sin(dlat / 2)) +
         (math.cos(math.radians(latx)) * math.cos(math.radians(laty)) *
          math.sin(dlon / 2) * math.sin(dlon / 2)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def calc_rtt_inf(rtt, dist, speed=300.0):
    """Compute RTT inflation from the (one-way) distance (in km) and the speed
    (in km/ms).
    """
    # Expected RTT when data travels at `speed`.
    crtt = (2 * dist)/speed
    return rtt/crtt


def compute_inf(m, locs):
    """Convert observed RTTs into inflation values.
    """
    for r in m:
        for c in m[r]:
            dist = calc_dist(locs[r], locs[c])
            m[r][c] = round(calc_rtt_inf(m[r][c], dist), const.PREC)
    return m


# Complete the symmetric matrix given the lower-left triangle.
complete_matrix = lambda m: utils.complete_matrix(m, const.NO_RTT)


def show_matrix(m):
    """Display cells of the matrix.
    """
    for r in sorted(m.keys()):
        for c in sorted(m[r].keys()):
            print("%20s %-20s %+2d" % (r, c, m[r][c]))
