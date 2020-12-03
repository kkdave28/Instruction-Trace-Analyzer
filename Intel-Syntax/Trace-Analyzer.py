#!/usr/bin/env python3
from os import replace, write
import sys
list_a = ['ah', 'al', 'eax', 'rax', 'ax']
list_b = ['bh', 'bl', 'ebx', 'rbx', 'bx']
list_c = ['ch', 'cl', 'ecx', 'rcx', 'cx']
list_d = ['dh', 'dl', 'edx', 'rdx', 'dx']
list_si = ['rsi', 'esi', 'si', 'sil']
list_di = ['rdi', 'edi', 'di', 'dil']
b_p = 1
w_p = 2 * b_p
dw_p = 2 * w_p
qw_p = 4 * w_p
size_directive_lookups = {"BYTE PTR":b_p, "WORD PTR": w_p, "DWORD PTR":dw_p, "QWORD PTR":qw_p}
global_instruction_list = []

def same_register_set(rega, regb):
    return((rega in list_a and regb in list_a)or(rega in list_b and regb in list_b)or (rega in list_c and regb in list_c)or(rega in list_d and regb in list_d)or(rega in list_si and regb in list_si)or(rega in list_di and regb in list_di))
def generate_trace(i_file: str, o_file: str)-> str:
    try:
        input = open(i_file, "r")
        output = open(o_file, "w")
    except Exception as e:
        print(e)
        return -1
    instruction_index = 1
    
    is_crashing_instruction = False
    while True:
        line = input.readline()
        effective_addr = 0x0
        if line == "": #EOF
            break
        elif line.find("=>") != -1:
            line = line.replace("=>","")
            line = line.split("#",1)[0].strip()
            main_list = line.strip().split(" ",1)
            register_lookup_table = {}
            inst_output = line
            for i in range(0,24):
                line = input.readline()
                entry_list = line.split()
                if i==0 and entry_list[0] != "rax": #crashing instruction is printed once again in the GDB output and is the last intruction printed without register output
                    is_crashing_instruction = True
                    break
                else:
                    register_lookup_table[entry_list[0]] = entry_list[1]
            instruction = main_list[0]
            tracing_list = []
            tracing_list.append(instruction)
            if is_crashing_instruction:
                output.write(" \n**CRASHING INSTRUCTION** "+str(instruction_index-1)+": "+inst_output.strip())
                global_instruction_list.pop(len(global_instruction_list)-1)
                return inst_output.strip()
            else:
                output.write(str(instruction_index)+": "+inst_output.strip())
            if len(main_list) > 1:
                operands = main_list[1].strip().split(",")
                tracing_list.append([x for x in operands])
                
                for o in range(0,len(operands)):
                    output.write("  Operand Values: ")
                    op = operands[o]
                    if op.find("[") != -1 and op.find("]") != -1 and o == 0:
                        for keys in register_lookup_table.keys():
                            if op.find(keys) != -1:
                                output.write(keys + " = " + register_lookup_table[keys]+", ")
                            operands[o] = operands[o].replace(keys, register_lookup_table[keys]) # replace register names with values.
                        addr_str = operands[o][operands[o].find("[")+1:operands[o].find("]")]
                        effective_addr = eval(addr_str)
                        ptr_type = op[:op.find('[')-1]
                        if ptr_type in size_directive_lookups.keys():
                            tracing_list.append([x for x in range(effective_addr, effective_addr+size_directive_lookups[ptr_type])])
                       # print(tracing_list)
                        output.write(" *STORE* ")
                        output.write(" Effective Address = " + hex(effective_addr))
                    elif op.find("[") != -1 and op.find("]") != -1 and o == 1:
                        for keys in register_lookup_table.keys():
                            if op.find(keys) != -1:
                                output.write(keys + " = " + register_lookup_table[keys]+", ")
                            operands[o] = operands[o].replace(keys, register_lookup_table[keys]) # replace register names with values.
                        addr_str = operands[o][operands[o].find("[")+1:operands[o].find("]")]
                        effective_addr = eval(addr_str)
                        ptr_type = op[:op.find('[')-1]
                        if ptr_type in size_directive_lookups.keys():
                            tracing_list.append([x for x in range(effective_addr, effective_addr+size_directive_lookups[ptr_type])])
                        output.write(" *LOAD* ")
                        output.write(" Effective Address = " + hex(effective_addr)) # evaluate the expression to get the effective address
                    elif op in register_lookup_table.keys():
                        output.write(register_lookup_table[op])
                    else:
                        output.write
                    #print(op)
                #print(operands)
            output.write("\n")
            if(len(tracing_list) != 0):
                global_instruction_list.append(tracing_list)
            instruction_index+=1
    return ""

def trace_corrupting_instruction(corrupting_inst:str):
    if(corrupting_inst == ""):
        return
    instruction_list = corrupting_inst.split()
    operand_list = instruction_list[1].split(",",1)
    corrupted_op = ""
    corrupted_memory_addrs = []
    if(len(operand_list)<=1):
        corrupted_op = operand_list[0]
        #print(corrupted_reg)
    else:
        corrupted_op = operand_list[1]
        #print(corrupted_reg)
   
    if(corrupted_op.find("[") != -1):
        print("corruption point found: " + corrupted_op+"\n")
    else:
        for x in reversed(global_instruction_list):
            #print(x)
            if(len(x) <= 1 ): # need to add support for instructions that reference registers implicitly.
                continue
            else:
                if(len(x[1]) > 1):
                    if(len(corrupted_memory_addrs) != 0):
                        if(x[1][0].find('[') != -1):
                            for y in corrupted_memory_addrs:
                                if y in x[2]:
                                    print("Most likely corrupting instruction found: "+ x[0]+ str(x[1]))
                                    corrupted_op = x[1][1]
                                    break
                    if(x[1][0] == corrupted_op or same_register_set(corrupted_op, x[1][0])):
                        if(x[1][1].find("[") !=-1):
                            #print(x)
                            corrupted_memory_addrs = x[2]
                            #print("corrupting instruction found  " + x[0] + str(x[1]))
                        else:
                            corrupted_op = x[1][1]

    

def main(argv:list):
    if len(argv) < 3:
        print("Error: Not enough arguments given")
        return -1
    corrupting_inst = generate_trace(argv[1], argv[2])
    trace_corrupting_instruction(corrupting_inst)

if __name__ == "__main__":
    main(sys.argv)