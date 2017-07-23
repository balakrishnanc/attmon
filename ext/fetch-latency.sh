#!/usr/bin/env bash
# -*- mode: sh; coding: utf-8; fill-column: 80; -*-
#
# fetch-latency.sh
# Created by Balakrishnan Chandrasekaran on 2017-06-23 04:54 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#


function crash() {
    echo "Error: $1" >& 2
    exit 1
}


# Ensure that `curl` is installed.
[ -z `which curl` ] && crash '`curl` not found!'
CURL=`which curl`


# Output directory path and file name.
readonly SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly OUT_PATH="$SRC_DIR/../data/latency"
readonly OUT_FILE="$OUT_PATH/att-network-delay--`date '+%H%M-%m%d%Y'`.html"

# URL to fetch.
readonly URL='http://ipnetwork.bgtmo.ip.att.net/pws/network_delay.html'


$CURL -o $OUT_FILE $URL
