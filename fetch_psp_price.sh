#!/bin/bash
fetch_tomorrow=false
while getopts t flag
do
    case "${flag}" in
        t) fetch_tomorrow=true;;
    esac
done

cd "$(dirname "$0")"
source venv/bin/activate
if [ "$fetch_tomorrow" = true ] ; then
    python3 psp_parser.py -t
else
    python3 psp_parser.py
fi