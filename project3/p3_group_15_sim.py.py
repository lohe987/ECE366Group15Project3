# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:17:41 2018

@author: USER
"""
def simulate(I,Nsteps,Memory):
    print("ECE366 Fall 2018 ISA Design: Simulator")
    print()
    PC = 0              # Program-counter
    DIC = 0
    Reg = [0,0,0,0]     # 4 registers, init to all 0
    print("******** Simulation starts *********")
    finished = False
    input_prog1 = open("p3_group_15_p1_imem.txt", "r")
    input_prog2 = open("p3_group_15_p2_imem.txt", "r")
    input_pattA = open("p3_group_15_dmem_A.txt", "r")
    input_pattB = open("p3_group_15_dmem_B.txt", "r")
    input_pattC = open("p3_group_15_dmem_C.txt", "r")
    input_pattD = open("p3_group_15_dmem_D.txt", "r")
    output_pattA = open("p3_group_15_dmem_A.txt", "w")
    output_pattB = open("p3_group_15_dmem_B.txt", "w")
    output_pattC = open("p3_group_15_dmem_C.txt", "w")
    output_pattD = open("p3_group_15_dmem_D.txt", "w")
    while(not(finished)):
        fetch = I[PC]
        DIC += 1
        #if(debug_mode):
            #print(fetch)
        #fetch = fetch.replace("R","")       # Delete all the 'R' to make things simpler
        if (fetch[1:4] == "101"):
            op  = "INIT"
            rx = str(int(fetch[4:6], 2))
            const = str(int(fetch[6:8], 2))
            Reg[rx] = const
            output = op + " r" + rx + ", " + const + " //rx = imm\n"
            PC += 1
            
        elif (fetch[1:4] == "111"):
            op = "ADDI"
            rx = str(int(fetch[4:6], 2))
            const = str(int(fetch[6:8], 2))
            Reg[rx] = rx + const
            output = op + " r" + rx + ", " + const + " //rx = rx + imm\n"
            PC += 1

        elif (fetch[1:4] == "100"):
            op = "ADD"	
            rx = str(int(fetch[4:6], 2))
            ry = str(int(fetch[6:8], 2))
            Reg[rx] = rx + ry
            output = op + " r" + rx + ", " + ry + " //rx = rx + ry\n"
            PC += 1
            
        elif (fetch[1:4] == "010 "):    #jif
            op = "JIF"
            const = str(int(fetch[4:8], 4))
            PC = PC + const
        elif (fetch[1:4] == "001 "):
            op = "lw"      
            
            PC += 1
        elif (fetch[0:4] == "load"):
            fetch = fetch.replace("load ","")
            fetch = fetch.replace("(","")
            fetch = fetch.replace(")","")
            fetch = fetch.split(",")
            Rx = int(fetch[0])
            Ry = int(fetch[1])
            Reg[Rx] = Memory[Ry]
            PC += 1
        elif (fetch[0:4] == "stre"):
            fetch = fetch.replace("stre ","")
            fetch = fetch.replace("(","")
            fetch = fetch.replace(")","")
            fetch = fetch.split(",")
            Rx = int(fetch[0])
            Ry = int(fetch[1])
            Memory[Reg[Ry]] = Reg[Rx]
            PC += 1
        elif (fetch[0:4] == "slt0"):  # why "slt0" instead of "sltR0" ? 
                                    # --> because all the 'R' is deleted at fetch to make things simplier. 
            fetch = fetch.replace("slt0 ","")
            fetch = fetch.split(",")
            Rx = int(fetch[0])
            Ry = int(fetch[1])
            if( Reg[Rx] < Reg[Ry] ):
                Reg[0] = 1
            else:
                Reg[0] = 0
            PC += 1
        elif (fetch[0:4] == "bez0"):
            fetch = fetch.replace("bez0 ","")
            fetch = fetch.split(",")
            imm = int(fetch[0])
            if ( Reg[0] == 0):
                PC = PC + imm
            else:
                PC += 1
        elif (fetch[0:4] == "jump"):
            fetch = fetch.replace("jump ","")
            fetch = fetch.split(",")
            imm = int(fetch[0])
            if(imm == 0):
                finished = True
            else:
                PC = PC + imm
            
        elif(fetch[0:8] == "00000000"):
            op = "HLT"
            finished = True
            
#        if(debug_mode):
#            if ( (DIC % Nsteps) == 0): # print stats every Nsteps
#                print("Registers R0-R3: ", Reg)
#                print("Program Counter : ",PC)
#                #print("Memory: ",Memory)   # Dont print memory atm. 
#                                            # Too much cluster
#                input("Press any key to continue")
#               print()
#        else:
#            continue
        
    print("******** Simulation finished *********")
    print("Dynamic Instr Count: ",DIC)
    print("Registers R0-R3: ",Reg)
    #print("Memory :",Memory)

    data = open("d_mem.txt","w")    # Write data back into d_mem.txt
    for i in range(len(Memory)):
        
        data.write(format(Memory[i],"016b"))
        data.write("\n")
        data.close()
        
def main():
    instr_file = open("p3_group_15_p1_imem.txt","r") #this is the machine code that has the instructions for prog 1
    data_file = open("p3_group_15_dmem_A.txt","r") #this is the machine code of data that professor provided 
    Memory = [] #the data will be stored in this
    #debug_mode = False  # is machine in debug mode?  
    Nsteps = 3          # How many cycle to run before output statistics
    Nlines = 0          # How many instrs total in input.txt  
    Instruction = []    # all instructions will be stored here
   
    #Simulation                       
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
    
    simulate(Instruction,Nsteps,Memory)
    
    instr_file.close()
    data_file.close()
    
if __name__ == "__main__":
    main()  
