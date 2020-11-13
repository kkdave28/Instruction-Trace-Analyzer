echo "b main
r "$@"
set logging on
set height 0
set disassembly-flavor intel
while 1
x/i \$pc
stepi
i r
end
x/i \$pc
stepi
i r 
quit
" > gdb-script.txt