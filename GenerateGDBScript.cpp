#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char const * argv[])
{
    std::string mainscript = "b main\nrun\n";
    std::string argscript = mainscript;
    std::string mainscript_intel = mainscript;
    mainscript_intel += "set disassembly-flavor intel\n";
    int bp = std::stoi(argv[1])-1;
    mainscript+="set variable $loop = *main +" + std::to_string(bp)+ std::string("\nset logging on\nset height 0\nwhile $pc != $loop\nx/i $pc\nstepi\nend\nx/i $pc\nquit");
    argscript+="set variable $loop = *main +" + std::to_string(bp)+ std::string("\nset logging on\nset height 0\nwhile $pc != $loop\nx/i $pc\nstepi\ni r\nend\nx/i $pc\nstepi\ni r\nquit");
    mainscript_intel+=mainscript;
    std::ofstream output_file;
    output_file.open("gdb-script");
    output_file<<mainscript;
    output_file.close();
    output_file.open("gdb-script-intel");
    output_file<<mainscript_intel;
    output_file.close();
    output_file.open("gdb-arg-script");
    output_file<<argscript;
    output_file.close();
    return 0;
}