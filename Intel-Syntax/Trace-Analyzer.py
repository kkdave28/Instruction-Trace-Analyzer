#!/usr/bin/env python3
from os import replace, write
import sys
import itertools
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
MODE = 64
reg_end_range = 24
size_directive_lookups = {"BYTE PTR":b_p, "WORD PTR": w_p, "DWORD PTR":dw_p, "QWORD PTR":qw_p}
global_instruction_list = []
register_list = list(itertools.chain(list_a, list_b, list_c, list_d, list_si, list_di))
if MODE == 32:
    reg_end_range = 16
def debug_prt(s, flag=0):
    if flag == 1:
        print(s)
def same_register_set(rega, regb):
    return((rega in list_a and regb in list_a)or(rega in list_b and regb in list_b)or (rega in list_c and regb in list_c)or(rega in list_d and regb in list_d)or(rega in list_si and regb in list_si)or(rega in list_di and regb in list_di))
def synonymous_reg_table(register_dict: dict)-> dict:
    """
        function to extract eax ax ah al and other values from rax for all x86 GP registers
    """
    """
        RAX/RBX/RCX/RDX
    """
    if(MODE == 32):
        register_dict["eiz"] = str(0x0)
    if(MODE == 64):
        register_dict["eax"] = (hex(int(register_dict["rax"],16) & 0x00000000ffffffff))
    register_dict["ax"]  = (hex(int(register_dict["eax"],16) & 0x0000ffff))
    register_dict["ah"]  = (hex((int(register_dict["ax"],16) & 0xff00)>>8))
    register_dict["al"]  = (hex(int(register_dict["ax"],16) & 0x00ff))

    if(MODE == 64):
        register_dict["ebx"] = (hex(int(register_dict["rbx"],16) & 0x00000000ffffffff))
    register_dict["bx"]  = (hex(int(register_dict["ebx"],16) & 0x0000ffff))
    register_dict["bh"]  = (hex((int(register_dict["bx"],16) & 0xff00)>>8))
    register_dict["bl"]  = (hex(int(register_dict["bx"],16) & 0x00ff))

    if(MODE == 64):
        register_dict["ecx"] = (hex(int(register_dict["rcx"],16) & 0x00000000ffffffff))
    register_dict["cx"]  = (hex(int(register_dict["ecx"],16) & 0x0000ffff))
    register_dict["ch"]  = (hex((int(register_dict["cx"],16) & 0xff00)>>8))
    register_dict["cl"]  = (hex(int(register_dict["cx"],16) & 0x00ff))

    if(MODE == 64):
        register_dict["edx"] = (hex(int(register_dict["rdx"],16) & 0x00000000ffffffff))
    register_dict["dx"]  = (hex(int(register_dict["edx"],16) & 0x0000ffff))
    register_dict["dh"]  = (hex((int(register_dict["dx"],16) & 0xff00)>>8))
    register_dict["dl"]  = (hex(int(register_dict["dx"],16) & 0x00ff))

    """
        RSP/RBP/RSI/RDI
    """
    if(MODE == 64):
        register_dict["esp"] = (hex(int(register_dict["rsp"],16) & 0x00000000ffffffff))
    register_dict["sp"]  = (hex(int(register_dict["esp"],16) & 0x0000ffff))
    register_dict["spl"]  = (hex(int(register_dict["sp"],16) & 0x00ff))

    if(MODE == 64):
        register_dict["ebp"] = (hex(int(register_dict["rbp"],16) & 0x00000000ffffffff))
    register_dict["bp"]  = (hex(int(register_dict["ebp"],16) & 0x0000ffff))
    register_dict["bpl"]  = (hex(int(register_dict["sp"],16) & 0x00ff))

    if(MODE == 64):
        register_dict["esi"] = (hex(int(register_dict["rsi"],16) & 0x00000000ffffffff))
    register_dict["si"]  = (hex(int(register_dict["esi"],16) & 0x0000ffff))
    register_dict["sil"]  = (hex(int(register_dict["si"],16) & 0x00ff))
    
    if(MODE == 64):
        register_dict["edi"] = (hex(int(register_dict["rdi"],16) & 0x00000000ffffffff))
    register_dict["di"]  = (hex(int(register_dict["edi"],16) & 0x0000ffff))
    register_dict["dil"]  = (hex(int(register_dict["di"],16) & 0x00ff))

    return register_dict

def generate_trace(i_file: str, o_file: str)-> str:
    crash = "rax"
    if(MODE == 32):
        crash = "eax"
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
            tracing_list = []
            tracing_list.append(instruction)
            if is_crashing_instruction:
                output.write(" \n**CRASHING INSTRUCTION** "+str(instruction_index-1)+": "+inst_output.strip())
                print(inst_output)
                global_instruction_list.pop(len(global_instruction_list)-1)

                return inst_output.strip()
            else:
                output.write(str(instruction_index)+": "+inst_output.strip())
            register_lookup_table = synonymous_reg_table(register_lookup_table)
            if len(main_list) > 1:
                operands = main_list[1].strip().split(",")
                tracing_list.append([x for x in operands])
                
                for o in range(0,len(operands)):
                    output.write("  Operand Values: ")
                    op = operands[o]
                    for keys in register_lookup_table.keys():
                        if op.find(keys) != -1:
                            output.write(keys + " = " + register_lookup_table[keys]+", ")
                            op = op.replace(keys, register_lookup_table[keys])
                        if op.startswith("0x"):
                            output.write("Constant = "+op)
                            break
                    operands[o] = op
                         # replace register names with values.
                    if op.find("[") != -1 and op.find("]") != -1 and o == 0:
                        addr_str = operands[o][operands[o].find("[")+1:operands[o].find("]")]
                        effective_addr = eval(addr_str)
                        ptr_type = op[:op.find('[')-1]
                        if ptr_type in size_directive_lookups.keys():
                            tracing_list.append([x for x in range(effective_addr, effective_addr+size_directive_lookups[ptr_type])])
                        output.write(" *STORE* ")
                        output.write(" Effective Address = " + hex(effective_addr))
                    elif op.find("[") != -1 and op.find("]") != -1 and o == 1:
                        addr_str = operands[o][operands[o].find("[")+1:operands[o].find("]")]
                        #print(addr_str)
                        effective_addr = eval(addr_str)
                        ptr_type = op[:op.find('[')-1]
                        if ptr_type in size_directive_lookups.keys():
                            tracing_list.append([x for x in range(effective_addr, effective_addr+size_directive_lookups[ptr_type])])
                        output.write(" *LOAD* ")
                        output.write(" Effective Address = " + hex(effective_addr)) # evaluate the expression to get the effective address
                    else:
                        output.write("")
                    #print(op)
                #print(operands)
            output.write("\n")
            if(len(tracing_list) != 0):
                global_instruction_list.append(tracing_list)
            instruction_index+=1
    return ""

def trace_corrupting_instruction(corrupting_inst:str, o_file: str):
    if(corrupting_inst == ""):
        return
    instruction_list = corrupting_inst.split(" ",1)
    operand_list = []
    print(instruction_list)
    if(instruction_list[1].find(",") != -1):
        operand_list = instruction_list[1].split(",",1)
    else:
        operand_list.append(instruction_list[1])
    print(operand_list)
    print(instruction_list)
    corrupted_op = ""
    output = open(o_file, "a")
    corrupted_memory_addrs = []
    if(len(operand_list)<=1):
        corrupted_op = operand_list[0]
        #print(corrupted_reg)
    else:
        corrupted_op = operand_list[1]
        #print(corrupted_reg)
    index = len(global_instruction_list)
    """
        This snippet traces the most recent instruction before the crash that directly/indirectly wrote to a register that was the source operand(s) of the crashing instruction
    """
    corrupted_op_list = []
    corrupted_op_list.append(corrupted_op)
    if(corrupted_op.find("[") != -1):
        for reg in register_list:
            if(corrupted_op.find(reg) != -1):
                corrupted_op_list.append(reg)
        if(len(corrupted_op_list) == 0):
            print("corruption point found: " + corrupted_op+"\n")
            return

    for cop in corrupted_op_list:
        corrupted_op = cop
        index = len(global_instruction_list)
        print("cop",cop)
        for x in reversed(global_instruction_list):
            
            debug_prt(x)
            index -=1
            #if(len(x) <= 1 ): # need to add support for instructions that reference registers implicitly.
            if(len(x) > 1):
                if(len(x[1]) > 1):
                    if(len(corrupted_memory_addrs) != 0):
                        if(x[1][0].find('[') != -1):
                            for y in corrupted_memory_addrs:
                                if(len(x) > 2):
                                    if y in x[2]:
                                        if x[1][1] in register_list or x[1][1].find("0x") != -1:
                                            print("Possible corrupting instruction found: "+str(index+1)+ ": "+x[0]+" "+" ,".join(x[1]))
                                            output.write("\nPossible corrupting instruction found: "+str(index+1)+ ": "+x[0]+" "+" ,".join(x[1]))
                                            break
                                    else:
                                        corrupted_op = x[1][1]
                                else:
                                    corrupted_op = x[1][1]
                    elif(x[1][0] == corrupted_op or same_register_set(corrupted_op, x[1][0])):
                        if(x[1][1].find("[") != -1):
                            corrupted_memory_addrs = x[2]
                        elif x[1][1].find("0x") != -1:
                            print("Possible corrupting instruction found: "+str(index+1)+ ": "+x[0]+" "+" ,".join(x[1]))
                            output.write("\nPossible corrupting instruction found: "+str(index+1)+ ": "+x[0]+" "+" ,".join(x[1]))
                            break
                        else:
                            corrupted_op = x[1][1]
                        
            """
                The code below traces in addition to code above what instruction wrote to the memeory address corrupted recently
            """
            """
            if(len(x) <= 1 ): # need to add support for instructions that reference registers implicitly.
                continue
            else:
                if(len(x[1]) > 1):
                    if(len(corrupted_memory_addrs) != 0):
                        if(x[1][0].find('[') != -1):
                            for y in corrupted_memory_addrs:
                                if y in x[2]:
                                    print("Most likely corrupting instruction found: "+ x[0]+ str(x[1]))
                                    #return
                                   # corrupted_op = x[1][1]
                                    break
                    if(x[1][0] == corrupted_op or same_register_set(corrupted_op, x[1][0])):
                        if(x[1][1].find("[") !=-1):
                            #print(x)
                            corrupted_memory_addrs = x[2]
                            corrupted_op = x[1][0]
                           # print(corrupted_op)
                            #print("corrupting instruction found  " + x[0] + str(x[1]))
                        else:
                            corrupted_op = x[1][1]
            """
def main(argv:list):
    if len(argv) < 3:
        print("Error: Not enough arguments given")
        return -1
    corrupting_inst = generate_trace(argv[1], argv[2])
    trace_corrupting_instruction(corrupting_inst, argv[2])

if __name__ == "__main__":
    main(sys.argv)