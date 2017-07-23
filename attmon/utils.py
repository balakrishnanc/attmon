#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# utils.py
# Created by Balakrishnan Chandrasekaran on 2017-06-27 18:40 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

"""
utils.py
Utility methods
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>'
__version__ = '1.0'
__license__ = 'MIT'


from . import constants as const
from collections import defaultdict
import io


# Utility `file open` calls.
__open = lambda m: lambda f: io.open(f, m, encoding='utf-8')
f_rd = __open('r')
f_wr = __open('w')


def load_content(page_file):
    """Slurp content from the file.
    """
    return f_rd(page_file).read()


def load_city_data(locs_file):
    """Load city codes, abbreviations, and names from file.
    """
    # City abbreviation to city code.
    abbrv_to_code = {}
    # City name to city code.
    cname_to_code = {}
    for line in f_rd(locs_file):
        code, abbrv, cname = [v.upper() for v in
                              line.strip().split(const.COMMA)]
        if abbrv:
            abbrv_to_code[abbrv] = code
        if cname:
            cname_to_code[cname] = code
    return abbrv_to_code, cname_to_code


def load_locs(locs_file):
    """Load city-code to latitude-longitude coordinates from file.
    """
    city_locs = {}
    for line in f_rd(locs_file):
        city, locs = line.split(const.TAB)
        # Pick the first latitude-longitude coordinate as the city center.
        loc = tuple([float(v) for v in
                     locs.split(const.COMMA)[0].split(const.COLON)])
        city_locs[city] = loc
    return city_locs


def gen_gp_data(fm, stats, out, sep=const.COMMA):
    """Using a full matrix of values, generates data in a gnuplot-friendly
    format.
    """
    # Column names.
    cols = sorted(fm[list(fm.keys())[0]].keys())

    # Row names.
    rows = sorted(fm.keys())

    # Each row is a list of comma-separated values with the 'row name' in the
    #  first position.
    out.write(sep + sep.join([c for c in cols]) + const.NEWLINE)
    out.write(const.NEWLINE.join([sep.join([r] +
                                           [str(fm[r][c]) for c in cols])
                                  for r in rows]))
    out.write(const.NEWLINE)
    out.write("#> min./max./avg. : %s, %s, %s\n" % tuple([str(v) for v in stats]))


def complete_matrix(matrix, def_val):
    """Complete the symmetric matrix given the lower-left triangle.
    """
    # Function to build a new row of values.
    def_row = lambda: defaultdict(lambda: def_val)

    # Full matrix.
    full_m = defaultdict(def_row)

    for r in matrix.keys():
        for c in matrix[r].keys():
            full_m[r][c] = matrix[r][c]

            if c not in full_m:
                for c in matrix[r]:
                    full_m[c][r] = matrix[r][c]
            elif r not in full_m[c]:
                full_m[c][r] = matrix[r][c]
    return full_m
