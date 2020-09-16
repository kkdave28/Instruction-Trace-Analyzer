default:
	gcc 1.c -ggdb -o one
	gcc 2.c -ggdb -o two
	g++ GenerateGDBScript.cpp -o genscript
clean:
	rm -f one.* two output gdb.txt gdb-script a.out genscript gdb-arg-script gdb-script-intel *.ATTtrace *.INTELtrace one two.*