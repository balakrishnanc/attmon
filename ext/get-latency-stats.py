#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# get-latency-stats.py
# Created by Balakrishnan Chandrasekaran on 2017-07-31 15:30 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

"""
get-latency-stats.py
Read latency data from files, with each file corresponding to one backbone
link, and compute basic statistics on the data.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>'
__version__ = '1.0'
__license__ = 'MIT'


from collections import defaultdict as defdict
from datetime import datetime as dt
import argparse
import io
import math
import numpy as np
import os


FSLASH = u'/'
HYPHEN = u'-'
SPACE = u' '


EPOCH = dt(1970, 1, 1)


def to_utc_seconds(dt_tuple):
    """Convert the date-time information (tuple) into seconds since an epoch.
    """
    # Time information tuple format:
    # 6 23 2017 5 2
    # 6 23 2017 5 15
    mon, day, yr, hh, mm = dt_tuple
    return (dt(yr, mon, day, hh, mm) - EPOCH).total_seconds()


def load_data(fpath, beg_ts, end_ts):
    """Load latency data from file, and return the data as a list of
    measurements.
    """
    for row in (line.strip() for line in io.open(fpath, 'r', encoding='utf-8')):
        # Data format:
        # 6 23 2017 5 2 30
        # 6 23 2017 5 15 30

        cols = row.split()
        tstamp = tuple((int(v) for v in cols[:5]))

        ts = to_utc_seconds(tstamp)
        if ts < beg_ts or ts > end_ts:
            continue

        data = int(cols[-1])
        yield (ts, data)


def compute_stats(meas):
    """Compute simple statistics of measurements.
    """
    avg = np.mean(meas)
    sdev = np.std(meas)
    p25, p75, p5, p95 = np.percentile(meas, (25, 75, 5, 95))
    return tuple([round(v, 2) for v in (avg, sdev, p25, p75, p5, p95)])


def analyze(in_path, *opts):
    """Merge data in separate files and measure variations.
    """
    links = defdict(lambda: [])
    for fname in os.listdir(in_path):
        fpath = os.path.sep.join((in_path, fname))
        meas = [m for m in load_data(fpath, *opts)]
        ts = [v[0] for v in meas]
        min_ts = np.min(ts)
        max_ts = np.max(ts)
        stats = compute_stats([v[-1] for v in meas])
        yield (fname, min_ts, max_ts, stats)


def to_dt_tuple(dt_str):
    """Convert date string to date-time tuple.
    """
    HH, MM = 0, 0
    mon, day, yr = [int(v) for v in dt_str.split(FSLASH)]
    return (mon, day, yr, HH, MM)


def main(args):
    """Merge rtt data.
    """
    in_path = os.path.abspath(args.in_path)
    out_file = os.path.abspath(args.out_file)
    beg_ts = to_utc_seconds(to_dt_tuple(args.beg_dt))
    end_ts = to_utc_seconds(to_dt_tuple(args.end_dt))

    if not os.path.isdir(in_path):
        raise ValueError("Invalid input path!")

    with io.open(out_file, 'w', encoding='utf-8') as out:
        for cols in analyze(in_path, beg_ts, end_ts):
            link_name, _min_ts, _max_ts, stats = cols
            stats_info = SPACE.join((str(v) for v in stats))
            line = SPACE.join((str(v) for v in (link_name, stats_info)))
            out.write(u"%s\n" % (line))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('Retrieve latency data of links and ' +
                     'compute basic statistics to measure delay variations.'))
    parser.add_argument('in_path', metavar='in_path',
                        type=str,
                        help='Input path containing latency data')
    parser.add_argument('out_file', metavar='out_file',
                        type=str,
                        help='Output file path')
    parser.add_argument('--beg', dest='beg_dt', metavar='beg_dt',
                        type=str,
                        default='6/30/2017',
                        help='Beginning date')
    parser.add_argument('--end', dest='end_dt', metavar='end_dt',
                        type=str,
                        default='7/30/2017',
                        help='Ending date')
    args = parser.parse_args()
    main(args)
