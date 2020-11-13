#! /usr/bin/bash
make
./genscript `./get-end.sh "$1"`
gdb "$1" -x gdb-script > /dev/null
./instruction-filter.sh gdb.txt "$1.temp" "AT&T-FORMAT"
./argumentify.py "$1.temp" "$1.ATTtrace"
rm "$1.temp"
rm gdb.txt
gdb "$1" -x gdb-script-intel > /dev/null
./instruction-filter.sh gdb.txt "$1.temp" "INTEL-FORMAT"
./argumentify.py "$1.temp" "$1.INTELtrace"
rm "$1.temp"
rm gdb.txt