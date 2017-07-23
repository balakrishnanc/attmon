#!/usr/bin/env bash
# -*- mode: sh; coding: utf-8; fill-column: 80; -*-
#
# fetch-loss.sh
# Created by Balakrishnan Chandrasekaran on 2017-07-21 22:47 +0200.
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
readonly OUT_PATH="$SRC_DIR/../data/loss"
readonly OUT_FILE="$OUT_PATH/att-network-loss--`date '+%H%M-%m%d%Y'`.html"

# URL to fetch.
readonly URL='http://ipnetwork.bgtmo.ip.att.net/pws/network_loss.html'


$CURL -o $OUT_FILE $URL
