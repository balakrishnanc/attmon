#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# attmon.py
# Created by Balakrishnan Chandrasekaran on 2017-06-23 02:26 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

"""
attmon.py
Utility to invoke the AT&T data monitors --- rttmon.py and lossmon.py.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>'
__version__ = '1.0'
__license__ = 'MIT'


import argparse
import attmon.lossmon as lossmon
import attmon.rttmon as rttmon
import attmon.utils as utils
import sys


# Metrics to analyze.
DELAY = 'delay'
LOSS  = 'loss'
METRICS = (DELAY, LOSS)


def parse_delay(args, city_data):
    """Parse network delay matrix from the HTML file.
    """
    m, avg = rttmon.parse(utils.load_content(args.html_file), city_data)
    if args.locs_file:
        m = rttmon.compute_inf(m, utils.load_locs(args.locs_file))

    # Complete matrix.
    fm = rttmon.complete_matrix(m)

    return fm, avg


def parse_loss(args, city_data):
    """Parse network loss matrix from the HTML file.
    """
    m, avg = lossmon.parse(utils.load_content(args.html_file), city_data)

    # Complete matrix.
    fm = lossmon.complete_matrix(m)

    return fm, avg


def main(args):
    if args.metric not in METRICS:
        raise ValueError("Unsupported Metric: %s" % (args.metric))

    city_data = utils.load_city_data(args.city_file)

    if args.metric == DELAY:
        fm, avg = parse_delay(args, city_data)
    else:
        fm, avg = parse_loss(args, city_data)

    out = args.out_file
    if not args.out_file:
        out = sys.stdout
    else:
        out = utils.f_wr(args.out_file)

    with out:
        utils.gen_gp_data(fm, avg, out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Retrieve network delay matrix from HTML file')
    parser.add_argument('metric', metavar='metric',
                        type=str,
                        help=("'delay' or 'loss'"))
    parser.add_argument('html_file', metavar='input',
                        type=str,
                        help=('HTML file containing ' +
                              'the network delay/loss measurements'))
    parser.add_argument('--city-data', dest='city_file', metavar='city_file',
                        type=str,
                        default='data/city-code-abbrev-name.txt',
                        help=('Text file containing ' +
                              'city codes, abbreviations and names'))
    parser.add_argument('--locs', dest='locs_file', metavar='city-locations',
                        type=str,
                        help=('File containing ' +
                              'latitude-longitude coordinates for cities'))
    parser.add_argument('--out', dest='out_file', metavar='output',
                        type=str,
                        help=('File to which ' +
                              'the network delay/loss data will be written'))
    args = parser.parse_args()
    main(args)
