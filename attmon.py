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


import attmon.rttmon as rttmon
import io


# Utility `file open` calls.
__open = lambda m: lambda f: io.open(f, m, encoding='utf-8')
__rd = __open('r')
__wr = __open('w')


def load_content(page_file):
    """Slurp content from the file.
    """
    return __rd(page_file).read()


if __name__ == '__main__':
    m = rttmon.parse_page(load_content('test/att-network-delay--0217-06232017.html'))
    rttmon.show_matrix(m)
