#! /bin/bash
echo -n "$3" > "$2"
echo "" >> "$2"
cat "$1" | grep "=>" | awk '{ s = ""; for (i = 3; i <= NF; i++) s = s $i " "; print s }' | sed 's/<.*>: //'>> "$2"