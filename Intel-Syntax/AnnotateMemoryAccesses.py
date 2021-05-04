#!/usr/bin/env python3
from os import replace, write
import sys
import itertools
MODE = 64
reg_end_range = 24
if MODE == 32:
    reg_end_range = 16
def Annotate(i_file: str, o_file: str) -> None:
    try:
        input_file = open(i_file, "r")
        output_file = open(o_file, "w")
    except Exception as e:
        print(e)
        return -1
    instruction_index = 1
    crash = "rax"
    if(MODE == 32):
        crash = "eax"
    while True:
        line = input.readline()
        effective_addr = 0x0
        if line == "": #EOF
            break
        elif line.find("=>") != -1:
            line = line.replace("=>","")
            line = line.replace("   ", " ")
            line = line.split("#",1)[0].strip()
            print(line)
            main_list = line.strip().split(" ",1)
            register_lookup_table = {}
            inst_output = line
            for i in range(0,reg_end_range):
                line = input.readline()
                entry_list = line.split()
                if i==0 and entry_list[0] != crash: #crashing instruction is printed once again in the GDB output and is the last intruction printed without register output
                    is_crashing_instruction = True
                    break
                else:
                    register_lookup_table[entry_list[0]] = entry_list[1]
            instruction = main_list[0]
            if is_crashing_instruction:
                return
            if len(main_list) > 1:
                operands = main_list[1].strip().split(",")
            



def main(argv:list):
    if len(argv) < 3:
        print("Error: Not enough arguments given")
        return -1

if __name__ == "__main__":
    main(sys.argv)