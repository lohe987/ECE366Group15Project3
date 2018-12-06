# Authors: Kevin Calva
# This program is a simulator 
# Simulator has 2 modes:
#            Debug mode:  Execute program every # steps and
#                         output the state of each reg, and PC
#            Normal mode: Execute program all at once

def simulate(I,Nsteps,debug_mode,Memory):
    print("ECE366 Fall 2018 ISA Design: Simulator")
    print()
    PC = 0              # Program-counter
    DIC = 0
    Reg = [0,0,0,0]     # 4 registers, init to all 0
    special_reg_arr = [0, 0, 0, 0]
    branch = 0
    
    print("******** Simulation starts *********")
    finished = False
    while(not(finished)):
        fetch = I[PC]
        DIC += 1
        if(debug_mode):
            print(fetch)
        fetch = fetch.replace("R","")       # Delete all the 'R' to make things simpler
        if (fetch[1:4] == "000"):
            # ADD instruction
            print("ADD")
            rd = int(fetch[4:6], 2)
            rs = int(fetch[6:8], 2)
            Reg[rd] += int(Reg[rs])
            if(debug_mode):
                print(Reg)
            PC += 1
            
        elif (fetch[1:4] == "001"):
          # ADDI instruction
          print("ADDI")
          rd = int(fetch[4:6], 2)
          imm = int(fetch[6:8], 2)
          imm_values = [0, 1, -2, -1]#These are the only immediate values allowed to be added to registers
          Reg[rd] += imm_values[imm]
          PC += 1
        
        elif (fetch[1:4] == "010"):
            # SLT instruction
            print("SLT")
            rd = int(fetch[4:6], 2)
            rs = int(fetch[6:8], 2)
            # check if rd is smaller or not
            rd = Reg[rd]
            rs = Reg[rs]
            if (rd < rs):
                branch = 1   #condition is true
            elif (rd > rs or rd == rs):
                branch = 0   #condition is false
            PC += 1
        
        elif (fetch[1:4] == "100"):
            # B Instruction
            print("B")
            imm = int(fetch[4:8], 2)
            imm_values = [0, 1, 2, 3, 4, 5, 6, 7, -8, -7, -6, -5, -4, -3, -2, -1] #pass immediate from this array to be used in function
            imm = imm_values[imm]
            # b instruction (branch)
            if branch == 1:
                PC += imm
                # this instruction will branch based on SLT being true
            elif branch == 0:
                PC += 1
                
        elif (fetch[1:4] == "011"):
            # J instruction
            # instruction for jumping number of lines to new line location in program
            # the immediate number is number of lines ahead/backward pc will travel
            print("J")
            imm = int(fetch[4:8], 2)
            imm_values = [0, 1, 2, 3, 4, 5, 6, 7, -8, -7, -6, -5, -4, -3, -2, -1]
            imm = imm_values[imm]
            PC += imm
        
        elif (fetch[1:5] == "1010"):
            # load instruction
            print("LOAD")
            rd = int(fetch[5:7], 2)
            rs = int(fetch[7:8], 2)
            rs_value = Reg[rs]
            data_value = Memory[Reg[rs]]
            # Checks if memory address is out of range
            if (rs_value < 0 or rs_value > 108):
                print("OUT OF MEMORY BOUNDS:")
                PC += 1
            print("Data Value: ")
            print(data_value)
            # Negative Value
            value = 0
            if (data_value == 1):
                value = 0b1111111111111111 - data_value + 1 #take 2's compliment
                Reg[rd] = 0 - value
            else:   #this if else section helped us debug errors for our load instruction
                Reg[rd] = Memory[rs_value]
            PC += 1
            
        elif (fetch[1:5] == "1011"):
           # store instruction
           print("STORE")
           rd = int(fetch[5:7], 2)
           rs = int(fetch[7:8], 2)
           # converts into 16 bit binary value
           print("Reg value")
           print(Reg[rd])
           a = 0 #initiate a
           if (Reg[rd] < 0):
               print("NEGATIVE STORE")
               pos_value = 0 - Reg[rd] #this is meant store a negative value
               a = 0b1111111111111111 - pos_value + 1 #2's complement
               a = '{0:016b}'.format(a) #formating the 2's complemented value
           else:
                a = '{0:016b}'.format(Reg[rd])
           print("A")
           print(a) #this if else is meant for debugging to show us what's going on during the runtime of this simulator
           Memory[Reg[rs]] = a
           PC += 1
        
        elif (fetch[1:6] == "11000"):  # why "slt0" instead of "sltR0" ? 
                                    # --> because all the 'R' is deleted at fetch to make things simplier. 
            # left shift logic instruction
            print("LSL")
            rd = int(fetch[6:8], 2)
            dec_value = Reg[rd]
            a = ""
            if (dec_value < 0):
                print("NEGATIVE LEFT SHIFT")
                pos_value = 0 - dec_value #flip rd value
                a = 0b1111111111111111 - pos_value + 1 #obtain 2's C for debugging
                a = str('{0:016b}'.format(a)) #shows us base 2
                print("A: ", a)
            else: #This instruction was a pain because it would shift the decimal value from -20000 to -40000 which is technically out of range so in this if else statement you see where we got the idea for our method of debugging
                a = str('{0:016b}'.format(Reg[rd]))
            print("BINARY VALUE:  ", a)
            #bin_value = '{0:016b}'.format(int(a))#We adjust the binary value to accept a zero being added to it
            new_bin_str = a[1:16] + "0"#since we begin writing from [1:16] we can shift everything over to 0:15 then add the zero to LSB 
            print("new_bin_value: ", new_bin_str)
            if new_bin_str[0] == "1":
                value = 0b1111111111111111 - int(new_bin_str, 2) + 1
                Reg[rd] = 0 - value
            else:
                Reg[rd] = int(new_bin_str, 2)
            print("ORIGINAL VALUE: ", dec_value)
            print("NEW VALUE: ", Reg[rd])
            PC += 1
        
        elif (fetch[1:6] == "11001"):
           # nxor instruction
           print("NXOR")
           rd = int(fetch[6:7], 2)
           rs = int(fetch[7:8], 2)
           rd_value = Reg[rd]
           rs_value = Reg[rs]
           rd_bin = 0
           rs_bin = 0
           if (rd_value < 0): #this if else helps us properly perform 2's complement of a decimal number to binary
               pos_value = 0 - rd_value
               a = 0b1111111111111111 - pos_value + 1
               rd_bin = '{0:016b}'.format(a)
           else:
              rd_bin = '{0:016b}'.format(Reg[rd])
           if (rs_value < 0): #this also helps us change from deci to bin in 2's Complement
               pos_value = 0 - rs_value
               a = 0b1111111111111111 - pos_value + 1
               rs_bin = '{0:016b}'.format(a)
           else:
               rs_bin = '{0:016b}'.format(Reg[rs])


           nxor_value = ~(Reg[rd] ^ Reg[rs])#this performs the nxor bitwise computation
           nxor_bin = 0
           if (nxor_value < 0): #this if else helped us debug by seeing what value were computed
               pos_value = 0 - nxor_value
               a = 0b1111111111111111 - pos_value + 1
               nxor_bin = '{0:016b}'.format(a)
           else:
               nxor_bin = '{0:016b}'.format(Reg[rd])

           print("RD VALUE: ", rd_value)#These print statements helped us view what was going on during the instruction
           print("RS VALUE: ", rs_value)#They would allow us to debug this instruction more accurately
           print("NXOR VAL: ", nxor_value)
           print("RD BIN:   ", rd_bin)
           print("RS BIN:   ", rs_bin)
           print("NXOR BIN: ", nxor_bin)
           Reg[rd] = ~(Reg[rd] ^ Reg[rs])
           print()
           PC += 1
        
        elif (fetch[1:6] == "11010"):
             # EQZ instruction
             # this is the instruction for checking if rd = 0
             #if rd == 0 then branch = 1
             print("EQZ")
             rd = int(fetch[6:8], 2)
             if Reg[rd] == 0:
                 branch = 1
             else:
                branch = 0
             PC += 1
        
        elif (fetch[1:6] == "11011"):
            # COMP instruction
            # This performs the 2's complement of a number
            print("COMP")
            rd = int(fetch[6:8], 2)
            Reg[rd] *= -1
            PC += 1
        
        elif (fetch[1:6] == "11100"):
            # RCVP instruction
            # This retrieves $rd from a special register $srd
            print("RCVR")
            rd = int(fetch[6:8], 2)
            # our regular register receives specially stored values in a different array of registers
            Reg[rd] = special_reg_arr[rd]
            PC += 1
        
        elif (fetch[1:6] == "11101"):
            # RST instruction
            # this resets rd to equal 0
            print("RST")
            rd = int(fetch[6:8], 2)
            Reg[rd] = 0  # reset
            PC += 1
        
        elif (fetch[1:6] == "11110"):
            # STSH instruction
            # This saves value in rd to array of special registers indicated in srd
            # for example   reg_arr [0  1  2   rd]  rd is at location reg_arr[3]
            # so this "stashes" into special_reg_arr[3] as well in special_reg_arr[0 1 2 rd]
            print("STSH")
            rd = int(fetch[6:8], 2)
            special_reg_arr[rd] = Reg[rd]
            PC += 1
        
        elif(fetch[0:8] == "11111111"):
            finished = True
            # END
            print("END")
        if(debug_mode):
            if ( (DIC % Nsteps) == 0): # print stats every Nsteps
                print("Registers R0-R3: ", Reg)
                print("Program Counter : ",PC)
                #print("Memory: ",Memory)   # Dont print memory atm. 
                                            # Too much cluster
                input("Press any key to continue")
                print()
        else:
            continue
        
    print("******** Simulation finished *********")
    print("Dynamic Instr Count: ",DIC)
    print("Registers R0-R3: ",Reg)
    print("MEM[0]: P             ", Memory[0])
    print("MEM[1]: Q             ", Memory[1])
    print("MEM[2]: 6^P Mod Q     ", Memory[2])
    print("MEM[3]: Target Pattern", Memory[3])
    print("MEM[4]: Highest Score ", Memory[4])
    print("MEM[5]: Count         ", Memory[5])
    

def main():
    instr_file = open("p3_group_15_p2_imem.txt","r")
    data_file = open("p3_group_15_dmem_A.txt","r")
    Memory = []
    debug_mode = False  # is machine in debug mode?  
    Nsteps = 3          # How many cycle to run before output statistics
    Nlines = 0          # How many instrs total in input.txt  
    Instruction = []    # all instructions will be stored here
    print("Welcome to ECE366 ISA sample programs")
    print("Simulator")
    print("Simulator has 2 modes: ")
    print(" 1] Normal execution")
    print(" 2] Debug mode")
    simMode = int(input("Please select simulator's mode: "))
    if(simMode == 1):
        debug_mode = False
    elif(simMode == 2):
        debug_mode = True
        Nsteps = int(input("Debug Mode selected. Please enter # of debugging steps: "))
    else:
        print("Error, unrecognized input. Exiting")
        exit()
   
                       
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
    
    simulate(Instruction,Nsteps,debug_mode,Memory)

    instr_file.close()
    data_file.close()
    
if __name__ == "__main__":
    main()