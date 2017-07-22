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
import attmon.rttmon as rttmon
import attmon.utils as utils


def main(args):
    m = rttmon.parse(utils.load_content(args.html_file))
    if args.locs_file:
        m = rttmon.compute_inf(m, utils.load_locs(args.locs_file))

    # Complete matrix.
    fm = rttmon.complete_matrix(m)

    out = args.out_file
    if not args.out_file:
        out = sys.stdout
    else:
        out = utils.f_wr(args.out_file)

    with out:
        utils.gen_gp_data(fm, out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Retrieve network delay matrix from HTML file')
    parser.add_argument('html_file', metavar='input',
                        type=str,
                        help=('HTML file containing ' +
                              'the network delay measurements'))
    parser.add_argument('--locs', dest='locs_file', metavar='city-locations',
                        type=str,
                        help=('File containing ' +
                              'latitude-longitude coordinates for cities'))
    parser.add_argument('--out', dest='out_file', metavar='output',
                        type=str,
                        help=('File where ' +
                              'the network delay matrix should be written to'))
    args = parser.parse_args()
    main(args)
