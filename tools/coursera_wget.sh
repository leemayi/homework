#!/bin/bash

indexfile=index
cookiefile=cookie
[ -z "$cookiefile" ] && echo "Can't find cookie" && exit 1
wget --no-cookies --header "Cookie: $(cat $cookiefile)" "$@" -O $indexfile
python $(dirname $0)/coursera_parse.py $indexfile | tee download.sh | bash
