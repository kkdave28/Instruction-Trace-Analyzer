#!/usr/bin/env python3
import sys, re
"""
Overhaul of my spaghetti code that I wrote to parse the gdb trace of my program.
Will comment on every single line for sanity purposes.

Functions:
    main -> runs the program, takes in a list of strings to input/output files as argument;
    filter -> takes in 2 inputs from the command line called from main as input/output files.
"""
# list of operand matching patterns
pat_1 = re.compile("\(\%r..\)") # (%reg)
pat_2 = re.compile("-*0x\d+\(\%r..\)") # offset(%reg)
pat_3 = re.compile("-*0x\d+\(\%r..\,\%r..\,\d+\)") # offset(%reg_base,%reg_index,sizeofop)
canary = re.compile("\%fs:0x28")
def filter(input_file: str, output_file: str) -> None:
    """
    This function will take in 2 file names, open the files, read from input, 
    parse the input and push it to the output, additionally will also create a memory-instruction map described below.
    """
    try:
        i_file = open(input_file, "r") # open with read permissions
    except OSError:
        print("Error while opening file: "+input_file)
    except FileNotFoundError:
        print("Error: File "+input_file+" does not exist")
    
    try:
        o_file = open(output_file, "w") # open with write permissions
    except OSError:
        print("Error while opening file: "+output_file)
    except FileNotFoundError:
        print("Error: File "+output_file+" does not exist")
    index = 1
    while True:
        line = i_file.readline()
        if(line == ""):
            break
        if (line.find("=>") != -1):
            line = line.strip()
            main_list = line.split()
            register_dict = {}
            for i in range(0,24):
                line = i_file.readline()
                temp_list = line.split()
                if(len(temp_list) < 3):
                    break
                register_dict[temp_list[0]] = temp_list[1]
            main_list.pop(0)
            if(len(main_list) <= 0):
                continue
            o_file.write(" ".join(x for x in main_list))
            o_file.write("\n")
            main_list.pop(0)
            if(len(main_list) <= 0):
                continue
            main_list = main_list[0].split(",", 1)
            if(len(main_list) <= 1):
                operand = main_list[0]
               # operand = operand.replace("%", "")
                
                m = pat_1.match(operand)
                if m:
                    print("matched! ", m.group())

                continue


    i_file.close()
    o_file.close()

def main(argv: list) -> int:
    if(len(argv) < 3):
        raise Exception("Missing input/output file names.")
    else:
        filter(argv[1], argv[2])
    return 0

if __name__ == "__main__":
    main(sys.argv)