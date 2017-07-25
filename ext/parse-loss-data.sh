#!/usr/bin/env bash
# -*- mode: sh; coding: utf-8; fill-column: 80; -*-
#
# parse-loss-data.sh
# Created by Balakrishnan Chandrasekaran on 2017-07-25 12:49 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balac@inet.tu-berlin.de>.
#

readonly SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly ATTMON_BIN="$SRC_DIR/../attmon.py"
readonly CITY_DATA="$SRC_DIR/../data/city-code-abbrev-name.txt"

[ ! -e $ATTMON_BIN ]                        && \
    echo "Error: cannot find '$ATTMON_BIN'" && \
    exit 2

[ ! -e $CITY_DATA ]                        && \
    echo "Error: cannot find '$CITY_DATA'" && \
    exit 2


function show_usage() {
    echo "Usage: $0 <in-path> <out-path>" >& 2
    exit 1
}

[ $# -ne 2 ] && show_usage

readonly IN_PATH="$1"
readonly OUT_PATH="$2"

# Create output path if required.
[ ! -e $OUT_PATH ] && mkdir -p ${OUT_PATH}

for data_file in $(ls $IN_PATH/att-network-loss*.html); do
    ts_dt=$(basename $data_file | sed -E 's/^att-network-loss--(.*).html$/\1/')
    out_file="$OUT_PATH/$ts_dt.txt"

    dt=$(echo $ts_dt | cut -d'-' -f2)
    mon=$(echo $dt | cut -c1-2)
    day=$(echo $dt | cut -c3-4)
    yr=$(echo $dt | cut -c5-8)

    ts=$(echo $ts_dt | cut -d'-' -f1)
    hr=$(echo $ts | cut -c1-2)
    min=$(echo $ts | cut -c3-4)

    timestamp=$(echo "$mon $day $yr $hr $min")

    $ATTMON_BIN loss --city-data $CITY_DATA $data_file --as-adj-list | \
        grep -v '^#>'                                                | \
        tr ',' ' '                                                   | \
        tr -s ' '                                                    | \
        awk -v timestamp="$timestamp" '{print timestamp, $0}' > $out_file

    echo "$data_file  => $out_file"
done
