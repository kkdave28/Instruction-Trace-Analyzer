#! /usr/bin/env python3
import sys
def ATT_FORMAT(infile, outfile):
    index = 1
    while (True):
        line = infile.readline()
        if not line:
            break
        main_list = line.split(" ",1)
        instruction = main_list[0]
        main_list.pop(0)
        mem_access = False
        if(len(instruction) > 0):
            outfile.write("Instruction "+ str(index) +": "+instruction)
            index+=1
        if(len(main_list) <= 0):
            continue
        main_list = main_list[0].strip().split(",",1)
        if(len(main_list) >=1):
            if(main_list[0].find("(") != -1):
                if(len(main_list) == 1):
                    outfile.write("    <---MEM ACCESS-->")
                else:
                    outfile.write("    <---MEM ACCESS-->")
                    outfile.write("    ***LOAD***")
                mem_access = True
            elif(len(main_list) > 1 and main_list[1].find("(") != -1):
                outfile.write("    <---MEM ACCESS-->")
                outfile.write("    ***STORE***")
                mem_access = True
        if(not mem_access):
            outfile.write("    <---NON-MEM ACCESS-->")
        outfile.write("\n")
        for op in main_list:
            op = op.strip()
            if(len(op) <= 0):
                main_list.pop(0)
        if(len(main_list) > 0):
            for op in main_list:
                outfile.write("ARG = " + op + "\n")
        else:
            outfile.write("NO ARGS\n")
        outfile.write("-------------------------------------\n")
    return 0
def INTEL_FORMAT(infile, outfile):
    index = 1
    while (True):
        line = infile.readline()
        if not line:
            break
        main_list = line.split(" ",1)
        mem_access = False
        instruction = main_list[0]
        main_list.pop(0)
        if(len(instruction) > 0):
            outfile.write("Instruction "+ str(index) +": "+instruction)
            index+=1
        if(len(main_list) <= 0):
            continue
        main_list = main_list[0].strip().split(",",1)
        if(len(main_list) >=1):
            if(main_list[0].find("[") != -1):
                if(len(main_list) == 1):
                    outfile.write("    <---MEM ACCESS-->")
                else:
                    outfile.write("    <---MEM ACCESS-->")
                    outfile.write("    ***STORE***")
                mem_access = True
            elif(len(main_list) > 1 and main_list[1].find("[") != -1):
                outfile.write("    <---MEM ACCESS-->")
                outfile.write("    ***LOAD***")
                mem_access = True
        if (not mem_access):
            outfile.write("    <---NON-MEM ACCESS-->")
        outfile.write("\n")
        for op in main_list:
            op = op.strip()
            if(len(op) <= 0):
                main_list.pop(0)
        if(len(main_list)> 0):
            for op in main_list:
                outfile.write("ARG = " + op + "\n")
        else:
            outfile.write("NO ARGS\n")
        outfile.write("-------------------------------------\n")
        #print("\n")
    return 0
def main(argv: list):
    if(len(argv) < 3):
        print("Missing input and/or output file names")
        return -1 
    infile = open(argv[1], "r")
    outfile = open(argv[2], "w")
    line = infile.readline()
    if(line.strip() == "INTEL-FORMAT"):
        INTEL_FORMAT(infile,outfile)
    elif (line.strip() == "AT&T-FORMAT"):
        ATT_FORMAT(infile, outfile)
    return 0

if __name__ == "__main__":
    main(sys.argv)