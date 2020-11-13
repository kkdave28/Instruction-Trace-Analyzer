#! /bin/bash
#echo -n "$3" > "$2"
#echo "" >> "$2"
cat "$1" | sed '/^=>\|^[recsdefg]/!d' | sed 's/=>.*:\t/=> /' | sed 's/<.*>//' > "$2"