#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# merge-latency.py
# Created by Balakrishnan Chandrasekaran on 2017-07-25 15:45 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

"""
merge-latency.py
Merge latency data files and write the data for each link into a separate file.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>'
__version__ = '1.0'
__license__ = 'MIT'


from collections import defaultdict as defdict
import argparse
import io
import math
import os
import shutil
import sys


HYPHEN = u'-'
SPACE = u' '


def load_data(fpath, links):
    """Load latency data from file, and update the links with the data read from
    the file.
    """
    for row in (line.strip() for line in io.open(fpath, 'r', encoding='utf-8')):
        # Data format:
        # 07 21 2017 23 15 US-AZ-PHOENIX US-CA-LOSANGELES 11
        # 07 21 2017 23 15 US-AZ-PHOENIX US-CO-DENVER 37

        cols = row.split()
        tstamp = tuple((int(v) for v in cols[:5]))
        data = int(cols[-1])
        src_dst = tuple(cols[5:7])
        links[src_dst].append((tstamp, data))


def aggregate(in_path):
    """Merge data in separate files and aggregate them by link.
    """
    links = defdict(lambda: [])
    for fname in os.listdir(in_path):
        fpath = os.path.sep.join((in_path, fname))
        load_data(fpath, links)
    return links


def write_links(links, out_path):
    """Write data on each link to a separate file in the output directory.
    """
    for src_dst in links:
        fpath = os.path.sep.join((out_path, HYPHEN.join(src_dst)))
        links[src_dst].sort(key=lambda v: v[0])
        with io.open(fpath, 'w', encoding='utf-8') as f:
            for tstamp, data in links[src_dst]:
                f.write(u"%s %s\n" % (SPACE.join((str(v) for v in tstamp)), str(data)))


def summarize(links, out, thresh=0.0):
    """Summarize the data using simple statistics.
    """
    # Average latency of links.
    rtt_avg = []

    # Standard deviation of link latencies.
    rtt_std = []

    # Maximum latency observed on links.
    rtt_max = [] 

    for src_dst in links:
        data_lst = [v[1] for v in links[src_dst]]

        # Average latency.
        avg = sum(data_lst)/len(data_lst)
        rtt_avg.append((avg, src_dst))

        # Standard deviation of latencies.
        var = sum([(v-avg)**2 for v in data_lst])/(len(data_lst)-1)
        std = math.sqrt(var)
        rtt_std.append((std, src_dst))

        # Maximum latency.
        rtt_max.append((max(data_lst), src_dst))

    # Sort the data on links in reverse order.
    rtt_avg.sort(key=lambda v: v[0], reverse=True)
    rtt_std.sort(key=lambda v: v[0], reverse=True)
    rtt_max.sort(key=lambda v: v[0], reverse=True)

    out.write(u"*** links with highest average latency\n")
    for v, k in rtt_avg[:5]:
        out.write(u"    %4.2f %20s => %s\n" % (v, k[0], k[1]))

    out.write(u"*** links with highest standard deviation of latency\n")
    for v, k in rtt_std[:5]:
        out.write(u"    %4.2f %20s => %s\n" % (v, k[0], k[1]))

    out.write(u"*** links with maximum observed latency\n")
    for v, k in rtt_max[:5]:
        out.write(u"    %4.2f %20s => %s\n" % (v, k[0], k[1]))


def main(args):
    """Merge rtt data.
    """
    in_path = os.path.abspath(args.in_path)
    out_path = os.path.abspath(args.out_path)

    if not os.path.isdir(in_path):
        raise ValueError("Invalid input path!")

    if os.path.isdir(out_path) and args.wipe:
        shutil.rmtree(out_path)
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    links = aggregate(in_path)
    write_links(links, out_path)

    sumf = args.sum_file
    if not sumf:
        sumf = sys.stdout
    else:
        sumf = io.open(sumf, 'w', encoding='utf-8')

    with sumf:
        summarize(links, sumf)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('Retrieve latency data of links and ' +
                     'write them to separate files, one per link.'))
    parser.add_argument('in_path', metavar='in_path',
                        type=str,
                        help='Input path containing latency data')
    parser.add_argument('out_path', metavar='out_path',
                        type=str,
                        help='Output path')
    parser.add_argument('--wipe', dest='wipe',
                        action='store_true',
                        default=False,
                        help='Wipe clean the output path prior to run')
    parser.add_argument('--summary', dest='sum_file', metavar='summary_file',
                        type=str,
                        help='Output file for summaries')
    args = parser.parse_args()
    main(args)
