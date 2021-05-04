Main Working Directory is Intel Syntax.

Steps for running the code.

1. $ ./gen-gdbscript.sh `executable`
2. $ gdb `executable` -x `gdb-script.txt`
3. $ ./augmented-filter.sh `gdb.txt` `TraceOutputFile`
4. $ ./TraceAnalyzer.py `TraceOutputFile` `FinalOutputFile`

- additionally if you have gdb.txt already in the folder from previous trace, please delete it before proceeding to step 2. 

