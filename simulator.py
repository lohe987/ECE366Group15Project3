# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:17:41 2018

@author: USER
"""

def main():
    instr_file = open("both_prog.txt","r")
    data_file = open("d_mem.txt","r")
    Memory = []
    debug_mode = False  # is machine in debug mode?  
    Nsteps = 3          # How many cycle to run before output statistics
    Nlines = 0          # How many instrs total in input.txt  
    Instruction = []    # all instructions will be stored here
    print("Welcome to ECE366 ISA sample programs")
    print(" 1 = simulator")
    print(" 2 = disassembler")
    print(" 3 = assembler")
    mode = int(input("Please enter the mode of program: "))
    print("Mode selected: ",end="")
    if( mode == 1):
        print("Simulator")
        print("Simulator has 2 modes: ")
        print(" 1] Normal execution")
        print(" 2] Debug mode")
        simMode = int(input("Please select simulator's mode: "))
        if ( simMode == 1):
            debug_mode = False
        elif (simMode == 2):
            debug_mode = True
            Nsteps = int(input("Debug Mode selected. Please enter # of debugging steps: "))
        else:
            print("Error, unrecognized input. Exiting")
            exit()
    elif ( mode == 2):
        print("Disassembler")
    elif ( mode == 3):
        print("Assembler")
    else:
        print("Error. Unrecognized mode. Exiting")
        exit()
    #mode = 1            # 1 = Simulation 
                        # 2 = disassembler
                        # 3 = assembler
    for line in instr_file: # Read in instr 
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        line = line.replace("\n","")
        Instruction.append(line)                        # Copy all instruction into a list
        Nlines +=1

    for line in data_file:  # Read in data memory
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        Memory.append(int(line,2))
    
    if(mode == 1):   # Check wether to use disasembler or assembler or simulation 
        simulate(Instruction,Nsteps,debug_mode,Memory)
    elif(mode == 2):
        disassemble(Instruction,Nlines)
    else:
        assemble(Instruction,Nlines)

    
    instr_file.close()
    data_file.close()
    
if __name__ == "__main__":
    main()