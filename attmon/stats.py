#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# stats.py
# Created by Balakrishnan Chandrasekaran on 2017-07-23 15:27 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

"""
stats.py
Compute simple statistics of the delay or loss values gathered.
"""

__author__  = 'Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>'
__version__ = '1.0'
__license__ = 'MIT'


from collections import namedtuple as nt


# Simple statistics record: (minimum, maximum, and average).
Stats = nt('Stats', ('min', 'max', 'avg'))


def compute(matrix, missing_val):
    """Compute simple statistics on the gathered delay or loss values.
    """
    vals = [matrix[r][c]
            for r in matrix.keys()
            for c in matrix[r]
            if matrix[r][c] != missing_val]
    return Stats(min(vals), max(vals), sum(vals)/len(vals))
