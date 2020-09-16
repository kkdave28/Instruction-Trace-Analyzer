#! /usr/bin/env python3
import sys
def isLoadStore(instruction: str):
    return (instruction.find("mov") != -1 or instruction.find("add") != -1 or instruction.find("sub") != -1 or instruction.find("mul") != -1 or instruction.find("sal") != -1 or instruction.find("sar") != -1 or instruction.find("xor") != -1 or instruction.find("and") != -1 or instruction.find("or") != -1 or instruction.find("inc") != -1 or instruction.find("dec") != -1 or instruction.find("neg") != -1 or instruction.find("not") != -1 or instruction.find("shl") != -1 or instruction.find("shr") != -1 or instruction.find("rol") != -1 or instruction.find("ror") != -1 or instruction.find("rcl") != -1 or instruction.find("rcr") != -1 or instruction.find("sto") != -1 or instruction.find("lod") != -1)
def filter(input_file, output_file):
    index = 1
    load_store_map = {}
    load_store_file = output_file.name + ".lsmap"
    lsfile = open(load_store_file, "w")
    output_tuple=("Address", "L/S", "Inst#")
    lsfile.write('{0:<10} {1:>16} {2:>10}\n'.format(*output_tuple))
    while(True):
        line = input_file.readline()
        IsMemAcess = False
        memacctype = -1
        effective_address = -1
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
            #print(main_list)
            main_list.pop(0)
            if(len(main_list)<=0):
                continue
            instruction = main_list[0]
            main_list.pop(0)
            output_file.write("Instruction " + str(index)+": " + instruction+ "\n")
            
            if(len(main_list)> 0):
                main_list = main_list[0].split(",",1)
                if(len(main_list) > 1):
                    if(main_list[0].find("(") != -1 and main_list[1].find(")") != -1):
                        partition = main_list[1][0:main_list[1].find(")")+1]
                        concat = main_list[0] + "," + partition
                        main_list[1] = main_list[1].replace(partition+",","")
                        main_list.pop(0)
                        main_list.insert(0, concat)
                op_index = 0
                for operand in main_list:
                    output_file.write("Operand #"+ str(op_index)+": "+operand)
                    if(op_index == 0):
                        if(operand[0] == '-' or operand[0] == '0' or operand[0] == "*"):
                            operand = operand.replace("%","")
                            operand = operand.replace("(", ",")
                            IsMemAcess = True
                            memacctype = 0
                            operand = operand.replace(")", "")
                            operand = operand.replace("*","")
                            operand = operand.split(",")
                            for x in operand:
                                if(x == ''):
                                    operand.remove(x)
                            if(len(operand) > 1):
                                if(operand[1] == ''):
                                    operand.pop(1)
                                base_addr = int(register_dict[operand[1]],16)
                                offset = int(operand[0],16)
                                if(len(operand) == 3):
                                    op_size = int(operand[2],16)
                                    base_addr = base_addr * offset
                                effective_address = base_addr + offset
                                output_file.write("  ---> Effective Address = "+hex(effective_address))
                            else:
                                if(operand[0] in register_dict.keys()):
                                    effective_address = register_dict[operand[0]]
                                else:
                                    effective_address = operand[0]
                                output_file.write("  ---> Effective Address = "+effective_address)
                        elif(operand[0] == "("):
                            IsMemAcess = True
                            memacctype = 0
                            operand = operand.replace("(","")
                            operand = operand.replace(")","")
                            operand = operand.replace("%","")
                            operand = operand.split(",")
                            if(len(operand) > 1):
                                base_addr = int(register_dict[operand[0]], 16)
                                offset = int(register_dict[operand[1]], 16)
                                op_size = int(operand[2], 16)
                                effective_address = base_addr + (offset * op_size)
                                output_file.write("  ---> Effective Address = "+hex(effective_address))
                            else:
                                if(operand[0].find("0x") != -1):
                                    effective_address = operand[0]
                                    output_file.write("  ---> Effective Address = "+hex(effective_address))
                                else:
                                    effective_address = register_dict[operand[0]]
                                    output_file.write("  ---> Effective Address = "+register_dict[operand[0]])
                        
                    elif(op_index == 1):
                         if(operand[0] == '-' or operand[0] == '0' or operand[0] == "*"):
                            IsMemAcess = True
                            memacctype = 1
                            operand = operand.replace("%","")
                            operand = operand.replace("(", ",")
                            operand = operand.replace(")", "")
                            operand = operand.replace("*","")
                            operand = operand.split(",")
                            if(len(operand) > 1):
                                if(len(operand) == 2):
                                    base_addr = int(register_dict[operand[1]],16)
                                    offset = int(operand[0],16)
                                    effective_address = base_addr + offset
                                    output_file.write("  ---> Effective Address = "+hex(base_addr+offset))
                                elif(len(operand) == 4):
                                    base_addr = int(register_dict[operand[1]],16)
                                    offset = int(operand[0],16)
                                    mem_index = int(register_dict[operand[2]],16)
                                    mem_sz = int(operand[3],16)
                                    effective_address = base_addr+offset+(mem_index*mem_sz)
                                    output_file.write("  ---> Effective Address = "+hex(effective_address))
                            else:
                                effective_address = operand[0]
                                output_file.write("  ---> Effective Address = "+operand[0])
                    output_file.write("\n")
                    op_index+=1
            else:
                output_file.write("NO ARGS\n")
            if(IsMemAcess == True):
                output_file.write("***** MEMORY ACCESS *****\n")
                if(memacctype == 0  and isLoadStore(instruction)):
                    output_file.write("<------ LOAD OPERATION ------>\n")
                    output_tuple = (hex(effective_address), "LOAD", str(index))
                    #lsfile.write(hex(effective_address) + "                    "+"LOAD"+"                    "+str(index)+"\n")
                    lsfile.write('{0:<10} {1:>13} {2:>10}\n'.format(*output_tuple))
                elif(memacctype == 1  and isLoadStore(instruction)):
                    output_file.write("<------ STORE OPERATION ------>\n")
                    output_tuple = (hex(effective_address), "STORE", str(index))
                    #lsfile.write(hex(effective_address) + "                    "+"LOAD"+"                    "+str(index)+"\n")
                    lsfile.write('{0:<10} {1:>13} {2:>10}\n'.format(*output_tuple))
                else:
                    output_file.write("<------ BASIC MEMORY ACCESS ------>\n")
            output_file.write("---------------------------------------\n")
            index +=1
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