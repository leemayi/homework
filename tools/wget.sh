#!/bin/bash

 wget --no-cookies --header "Cookie: $(cat cookies.txt)" "$@"
