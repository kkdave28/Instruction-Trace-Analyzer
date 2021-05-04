#! /usr/bin/zsh
let endpoint=$(expr `./get-end.sh "$1"` - 1)
echo "b main
r "${@:2}"
set logging on
set height 0
set disassembly-flavor intel
set variable \$loop = *main + $endpoint
while \$pc != \$loop
x/i \$pc
nexti
i r
end
nexti
i r
quit" > "`pwd`/gdb-script.txt"
