#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# lossmon.py
# Created by Balakrishnan Chandrasekaran on 2017-07-23 01:07 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

"""
lossmon.py
Fetch network loss values reported by AT&T.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>'
__version__ = '1.0'
__license__ = 'MIT'


from . import constants as const
from . import stats
from . import utils
import io
import math


# Missing loss value.
NO_LOSS_VAL = float(const.NO_LOSS)


def proc_row(row):
    """Process data in the current row.
    """
    if len(row) == 1:
        return (None, None, row[-1])
    return (row[0], row[1:-1], row[-1])


def parse(page, city_data):
    """Parse Web page and report the loss matrix on the page.
    """
    # Mapping from abbreviations and city names to city codes.
    abbrvs, cnames = city_data
    # Flag indicating when to begin scanning.
    scan = False
    # Flag indicating when to begin processing table data.
    proc = False
    # Flag indicating the ID of the column we are parsing within a row.
    col_num = 0

    loss_matrix = {}
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

                val = const.NO_LOSS

            curr_row.append(val.strip())

        if const.ROW_END_PAT.match(line):
            src, losses, hdr = proc_row(curr_row)

            if not src and not losses:
                col_hdrs.append(abbrvs[hdr.upper()])
            elif len(losses) != len(col_hdrs):
                raise ValueError('Unknown data format!')
            else:
                cc = cnames[src.upper()]
                loss_matrix[cc] = {dst:float(loss)
                                   for dst,loss in zip(col_hdrs, losses)}
                col_hdrs.append(abbrvs[hdr.upper()])

            curr_row = []


        if proc and const.TAB_END_PAT.match(line):
            break

    return loss_matrix, stats.compute(loss_matrix, NO_LOSS_VAL)


# Complete the symmetric matrix given the lower-left triangle.
complete_matrix = lambda m: utils.complete_matrix(m, const.NO_LOSS)


def show_matrix(m):
    """Display cells of the matrix.
    """
    for r in sorted(m.keys()):
        for c in sorted(m[r].keys()):
            print("%20s %-20s %3.1f" % (r, c, m[r][c]))
