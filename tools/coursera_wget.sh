#!/bin/bash

indexfile=index
if [ -f $indexfile ]; then
    read -p "index exists, download again ? [Y|n] " C
    if [ "$C" != n ] && [ "$C" != N ]; then
        cookiefile=cookie
        [ -z "$cookiefile" ] && echo "Can't find cookie" && exit 1
        wget --no-cookies --header "Cookie: $(cat $cookiefile)" "$@" -O $indexfile
    fi
fi
python $(dirname $0)/coursera_parse.py $indexfile | bash -x
