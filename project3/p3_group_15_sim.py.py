# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:17:41 2018

@author: Kevin Calva
"""
def simulate(I,Memory):
    print("ECE366 Fall 2018 ISA Design: Simulator")
    print()
    PC = 0              # Program-counter
    DIC = 0
    Reg = [0,0,0,0]     # 4 registers, init to all 0
    print("******** Simulation starts *********")
    finished = False
    while(not(finished)):
        fetch = I[PC]
        DIC += 1
        #if(debug_mode):
            #print(fetch)
        #fetch = fetch.replace("R","")       # Delete all the 'R' to make things simpler
        if (fetch[1:4] == "101"):
            #op  = "INIT"
            rx = int(fetch[4:6], 2)
            const = int(fetch[6:8], 2)
            Reg[rx] = const #Rx = const
            PC += 1 
            
        elif (fetch[1:4] == "111"):
            #op = "ADDI"
            rx = int(fetch[4:6], 2)
            const = int(fetch[6:8], 2)
            Reg[rx] = Reg[rx] + const #Rx = Rx + const
            PC += 1

        elif (fetch[1:4] == "100"):
            #op = "ADD"	
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:8], 2)
            Reg[rx] = Reg[rx] + Reg[ry] #Rx = Rx +Ry
            PC += 1
            
        elif (fetch[1:6] == "00000"):
            #op = "SUBR0"
            ry = int(fetch[6:8], 2)
            Reg[0] = Reg[0] - Reg[ry] #R0 = R0 -Ry
            PC += 1
			
        elif (fetch[1:5] == "0001"):
            #op = "XOR"
            rx = int(fetch[5:6], 2)
            ry = int(fetch[6:8], 2) 
            Reg[rx] = Reg[rx] ^ Reg[ry] #Rx = Rx XOR Ry
            PC += 1

        elif (fetch[1:4] == "001"):
            #op = "LWD"
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:8], 2)
            Reg[rx] = Memory[Reg[ry]] #Rx <- M[Ry]
            PC +=1

        elif (fetch[1:4] == "011"):
            #op = "SWD"
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:8], 2)
            Memory[Reg[ry]] = Reg[rx]  #Rx -> M[ry]
            PC += 1
            
        elif (fetch[1:4] == "110"):   
            #op = "SLE"
            rx = int(fetch[4:6], 2)
            ry = int(fetch[6:8], 2)
            if( Reg[rx] < Reg[ry] ): #Set less than (if Rx < Ry) Rx = 1  
                Reg[rx] = 1 
            else:
                Reg[rx] = 0
            PC += 1
        
        elif (fetch[1:8] == "1111100"):
            #op = "ADDN"
            #(Add negative one to r3)
            Reg[3] = Reg[3] - 1 #R3 = R3 + (-1)
            PC += 1
        
        elif (fetch[1:8] == "0001000"):
            #op = "CNTR0"
            output = op + " //Count the number of 1's in r0\n"
            Reg[3] = Reg[0]
            PC +=1
         
        elif (fetch[1:5] == "0000"):
            #op = "SLER"
            rx = int(fetch[5:7], 2)
            ry = int(fetch[7], 2)
            if(rx == 1):
                print("Rx CANNOT BE R1")
            if(ry != 0):
                print("Ry HAS TO BE R0!")
            if(Reg[rx] <= Reg[ry]):
                Reg[rx] = 1
            else:
                Reg[rx] = 0
            PC +=1
            
        elif (fetch[1:4] == "010"):
            #op = "JIF"
            const = int(fetch[5:8], 2)
            if(Reg[3] == 1):
                PC = PC + const
            else:
                PC += 1
        
        elif(fetch[1:8] == "0000000"):
            #op = "HLT"
            print("HALT")
            finished = False
            
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

    data = open("p3_group_15_dmem_A.txt","w")    # Write data back into d_mem.txt
    for i in range(len(Memory)):
        
        data.write(format(Memory[i],"016b"))
        data.write("\n")
        data.close()
        
def main():
    instr_file = open("p3._group_15_p1_imem.txt","r") #this is the machine code that has the instructions for prog 1
    data_file = open("p3_group_15_dmem_A.txt","r") #this is the machine code of data that professor provided 
    Memory = [] #the data will be stored in this
    #debug_mode = False  # is machine in debug mode?  
    #Nsteps = 3          # How many cycle to run before output statistics
    Nlines = 0          # How many instrs total in input.txt  
    Instruction = []    # all instructions will be stored here
    Instruction2 = []   # All Instructions for program 2 are stored here
    Memory2 = []        # Memory for program 2 is stored here
   
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
    
    simulate(Instruction,Memory)
    Nlines = 0;
    print("Program 1 complete. Now Begins Program 2: \n")
    instr_file = open("p3._group_15_p2_imem.txt","r") #this is the machine code that has the instructions for prog 2
    data_file = open("p3_group_15_dmem_A.txt","r") #this is the machine code of data that professor provided

    for line in instr_file: # Read in instr
        if (line == "\n" or line[0] == '#'):
            continue
        line = line.replace("\n", "")
        Instruction2.append(line)
        Nlines +=1
    for line in data_file: # Read in data memory
        if (line == "\n" or line[0] == '#'):
            continue
        Memory2.append(int(line,2))
    simulate(Instruction2,Memory)
    
    instr_file.close()
    data_file.close()
    
if __name__ == "__main__":
    main()  
