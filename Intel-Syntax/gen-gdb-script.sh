let endpoint=$(expr `./get-end.sh "$1"` - 1)
echo "b main
r "${@:2}"
set logging on
set height 0
set disassembly-flavor intel
set variable \$loop = *main + $endpoint
while \$pc != \$loop
x/i \$pc
stepi
i r
end
stepi
i r
quit" > gdb-script.txt