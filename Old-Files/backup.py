#! /usr/bin/env python3
import sys
def filter(input_file, output_file):
    index = 1
    while(True):
        line = input_file.readline()
        IsMemAcess = False
        memacctype = -1
        if(not line):
            break
        if(line.find("=>") != -1):
            line = line.strip()
            main_list = line.split()
            register_dict = {}
            for i in range(0,24):
                line = input_file.readline()
                temp_list = line.split()
                register_dict[temp_list[0]] = temp_list[1]
            #print(register_dict)
            main_list.pop(0)
            instruction = main_list[0]
            main_list.pop(0)
            output_file.write("Instruction " + str(index)+": " + instruction+ "\n")
            index +=1
            if(len(main_list)> 0):
                main_list = main_list[0].split(",",1)
                op_index = 0
                for operand in main_list:
                    output_file.write("Operand #"+ str(op_index)+": "+operand)
                    if(op_index == 0 and operand.find("(") != -1):
                        print(operand)
                        operand  = operand.replace("%","")
                        operand = operand.replace("(", ",")
                        operand = operand.replace(")", "")
                        operand = operand.replace("*","")
                        operand = operand.split(",")
                        print(operand)
                        if(len(operand) == 2):
                            if(operand[0] == ''):
                                output_file.write(" Effective Address = "+ register_dict[operand[1]] + "\n")
                            else:
                                print(operand)
                                offset = int(operand[0], 16)
                                base_addr = int(register_dict[operand[1]], 16)
                                effective_addr = base_addr + offset
                                output_file.write(" Effective Address = "+hex(effective_addr) + "\n")
                        elif(len(operand) == 4):
                            offset = int(operand[0],16)
                            base_addr = int(register_dict[operand[1]], 16)
                            mem_index = int(register_dict[operand[2]], 16)
                            op_size = int(operand[3], 16)
                            effective_addr = base_addr + offset + (mem_index * op_size)
                            output_file.write(" Effective Address = "+hex(effective_addr)+"\n")
                        IsMemAcess = True
                        memacctype = 0
                    elif(op_index == 1 and operand.find("(") != -1):
                        operand  = operand.replace("%","")
                        operand = operand.replace("(", ",")
                        operand = operand.replace(")", "")
                        operand = operand.replace("*","")
                        operand = operand.split(",")
                        print(operand)
                        if(len(operand) == 2):
                            if(operand[0] == ''):
                                output_file.write(" Effective Address = "+ register_dict[operand[1]] + "\n")
                            else:
                                offset = int(operand[0], 16)
                                base_addr = int(register_dict[operand[1]], 16)
                                effective_addr = base_addr + offset
                                output_file.write(" Effective Address = "+hex(effective_addr) + "\n")
                        elif(len(operand) == 4):
                            offset = int(operand[0],16)
                            base_addr = int(register_dict[operand[1]], 16)
                            mem_index = int(register_dict[operand[2]], 16)
                            op_size = int(operand[3], 16)
                            effective_addr = base_addr + offset + (mem_index * op_size)
                            output_file.write(" Effective Address = "+hex(effective_addr)+"\n")
                       # print(operand.strip().split(","))
                        IsMemAcess = True
                        memacctype = 1

                    elif(operand.find("0x") != -1 and operand.find("$") == -1):
                        IsMemAcess = True
                        memacctype = -1
                        output_file.write("\n")
                    else:
                        output_file.write("\n")
                    op_index+=1
                    

                
                
            else:
                output_file.write("NO ARGS\n")
            if(IsMemAcess == True):
                output_file.write("***** MEMORY ACCESS *****\n")
                if(memacctype == 0):
                    output_file.write("<------ LOAD OPERATION ------>\n")
                elif(memacctype == 1):
                    output_file.write("<------ STORE OPERATION ------>\n")
                else:
                    output_file.write("<------ BASIC MEMORY ACCESS ------>\n")
            output_file.write("---------------------------------------\n")
    return 0
def main(argv: list):
    if(len(argv) < 3):
        print("Missing input and/or output file names")
        return -1 
    infile = open(argv[1], "r")
    outfile = open(argv[2], "w")
    filter(infile, outfile)
    return 0
if __name__ == "__main__":
    main(sys.argv)