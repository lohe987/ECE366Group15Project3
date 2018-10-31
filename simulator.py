# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:17:41 2018

@author: USER
"""
def simulate(I,Nsteps,debug_mode,Memory):
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
        if(debug_mode):
            print(fetch)
        fetch = fetch.replace("R","")       # Delete all the 'R' to make things simpler
        if (fetch[0:4] == "init"):
            fetch = fetch.replace("init ","")
            fetch = fetch.split(",")
            R = int(fetch[0])
            imm = int(fetch[1])
            Reg[R] = imm
            PC += 1
        elif (fetch[0:4] == "addi"):
            fetch = fetch.replace("addi ","")
            fetch = fetch.split(",")
            R = int(fetch[0])
            imm = int(fetch[1])
            Reg[R] = Reg[R] + imm
            PC += 1
        elif (fetch[0:4] == "add "):
            fetch = fetch.replace("add ","")
            fetch = fetch.split(",")
            Rx = int(fetch[0])
            Ry = int(fetch[1])
            Reg[Rx] = Reg[Rx] + Reg[Ry]
            PC += 1
        elif (fetch[0:4] == "sub "):
            fetch = fetch.replace("sub ","")
            fetch = fetch.split(",")
            Rx = int(fetch[0])
            Ry = int(fetch[1])
            Reg[Rx] = Reg[Rx] - Reg[Ry]
            PC += 1
        elif (fetch[0:4] == "xor "):
            fetch = fetch.replace("xor ","")
            fetch = fetch.split(",")      
            Rx = int(fetch[0])
            Ry = int(fetch[1])
            Reg[Rx] = Reg[Rx] ^ Reg[Ry]
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
            
        elif(fetch[0:6] == "finish"):
            finished = True
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
    #print("Memory :",Memory)

    data = open("d_mem.txt","w")    # Write data back into d_mem.txt
    for i in range(len(Memory)):
        
        data.write(format(Memory[i],"016b"))
        data.write("\n")
        data.close()
    
def disassemble(I,Nlines):
    input_file = open("LIS_machine_code_program1.txt", "r")
    output_file = open("program1_disassembled.lis", "w")

    output = "\n"

    for line in input_file:
    	print (output)
    	output_file.write(output)
    
    	wrongOp = False
    	if (line == "\n"):
    		continue
    
    	line = line.replace("\n", "")
    	print ("Machine code: ", line)
    
    	op_bin = line[1:8]
    	if (op_bin == "0000000"):
    		op = "HLT"
    		output = op + " //Stop program\n" 
    		continue
    
    	elif (op_bin == "1111100"):
    		op = "ADDN"
    		output = op + "//r3 = r3 - 1\n" 
    		continue
    
    	elif (op_bin == "0001000"):
    		op = "CNTR0"
    		output = op + " //Count the number of 1's in r0\n"
    		continue
    	
    	op_bin = line[1:6]
    
    	if (op_bin == "00000"):
    		op = "SUBR0"
    		ry = str(int(line[6:8], 2)) 
    		if (ry == '1'):
    			wrongOp = True
    		if (wrongOp == False):
    			output = op + " r" + ry + " //r0 = r0 - ry\n"
    			continue
    
    	op_bin = line[1:5]
    	
    	if (op_bin == "0001"):
    		op = "XOR"
    		rx = str(int(line[5:6], 2))
    		ry = str(int(line[6:8], 2)) 
    		output = op + " r" + rx + ", r" + ry + " //rx = rx XOR ry\n"
    		continue
    
    	elif (op_bin == "0000"):
    		op = "SLER"
    		rx = str(int(line[5:7], 2))
    		ry = str(int(line[7], 2))
    		output = op + " r" + rx + ", r" + ry + " //If rx < r0 then r3 = 1\n\t//Else r3 = 0\n"
    		continue
    
    	op_bin = line[1:4]
    
    	if (op_bin == "100"):
    		op = "ADD"	
    		rx = str(int(line[4:6], 2))
    		ry = str(int(line[6:8], 2))
    		output = op + " r" + rx + ", " + ry + " //rx = rx + ry\n"
    		continue
    
    	elif (op_bin == "111"):
    		op = "ADDI"
    		rx = str(int(line[4:6], 2))
    		const = str(int(line[6:8], 2))
    		output = op + " r" + rx + ", " + const + " //rx = rx + imm\n"
    		continue
    
    	elif (op_bin == "001"):
    		op = "LWD"
    		rx = str(int(line[4:6], 2))
    		ry = str(int(line[6:8], 2))
    		output = op + " r" + rx + ", r" + ry + " //rx = M[ry]\n"
    		continue
    
    	elif (op_bin == "011"):
    		op = "SWD"
    		rx = str(int(line[4:6], 2))
    		ry = str(int(line[6:8], 2))
    		output = op + " r" + rx + ", r" + ry + " //M[ry] = rx\n"
    		continue
    
    	elif (op_bin == "110"):
    		op = "SLE"
    		rx = str(int(line[4:6], 2))
    		ry = str(int(line[6:8], 2))
    		output = op + " r" + rx + ", " + ry + " //If rx < ry then r3 = 1\n\t//Else r3 = 0\n"
    		continue
    
    	elif (op_bin == "101"):
    		op = "INIT"
    		rx = str(int(line[4:6], 2))
    		const = str(int(line[6:8], 2))
    		output = op + " r" + rx + ", " + const + " //rx = imm\n"
    		continue
    	
    	elif (op_bin == "010"):
    		op = "JIF"
    		sign = line[4] 
    		const = int(line[5:8], 2)
    		if (sign == '1'):
    			const = -(0b111 - int(const) + 1)
    
    		const = str(const)
    
    		output = op + " " + const + " //If r3 = 1 then jump (PC = PC + imm)\n\t//Else do nothing\n"
    		
    	print (output)
    	output_file.write(output)

def assemble(I,Nlines):
    input_file1 = open("program1.lis", "r")
    output_file = open("LIS_machine_code_program1.txt", "w")
    memSection = False
    codeSection = False
    #commentHere = False
    output = ""
    memory = []
    #jumpMarkers = dict()
    def TwosComplement(num, numBits):
        if (num < 0):
            num = (1 << numBits) + num
        else:
            if ((num & (1 << (numBits - 1))) != 0):
                num -= (1 << numBits)
        return num
        
    for line in input_file1:
        
        if (line == "\n"):
            continue
            
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        line = line.split('/')
        line = line[0]
        
        if (line == "*instructions"):
            memSection = False
            codeSection = True
        if (memSection == True):
            line = line.split('~')
            if (line[2][0] == '-'):
                line[2] = line[2].replace("-", "")
                line[2] = 0b1111111111111111 - int(line[2]) + 1
                
        memValue = format(int(line[2]), "016b")
        memory.append(memValue)
        
        if (line == "*memory"):
            memSection = True
        
        if (codeSection == True):
            line = line.replace("\t", "")
            line = line.replace("r", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
        
        if (line[0:3] == 'LWD'): 
            line = line.replace("LWD", "") 
            line = line.split(',')
            
            op = "001"
            
            rx = format(int(line[0]), "02b")
            const = format(int(line[1]), "02b")
            
            output = op + rx + const
        
        elif (line[0:3] == 'SWD'):
            line = line.replace("SWD", "")
            line = line.split(',')
            
            op = "011"
            rx = format(int(line[0]), "02b")
            const = format(int(line[1]), "02b")
            
            output = op + rx + const
        
        elif (line[0:4] == 'SLER'):
            line = line.replace("SLER", "")
            line = line.split(',')
            op = "0000"
            rx = format(int(line[0]), "02b")
            ry = format(int(line[1]), "01b")
            ry = ry[0]
            output = op + rx + ry
        
        elif (line[0:3] == 'SLE'):
            line = line.replace("SLE", "")
            line = line.split(',')
            
            op = "110"
            rx = format(int(line[0]), "02b")    		 	
            const = format(int(line[1]), "02b")
            output = op + rx + const
        
        elif (line[0:3] == 'SHL'):
            line = line.replace("SHL", "")
            line = line.split(',')
            
            op = "0001"
            rx = format(int(line[0]), "02b")
            const = format(int(line[1]), "01b")
            const = const[0]
            
            output = op + rx + const
        
        elif (line[0:4] == 'ADDN'):
            line = line.replace("ADDN", "")
            op = "1111"
            output = op + "100" 
        elif (line[0:4] == 'ADDI'):
            line = line.replace("ADDI", "")
            line = line.split(',')
            const = int(line[1])
            if (const < 0):
                const *= -1
                const = 0b1111111111111111 - const + 1
                const = format(const, "02b")
                const = const[14:16]
            else:
                const = format(int(line[1]), "02b")
                op = "111"
                rx = format(int(line[0]), "02b")
                output = op + rx + const
        elif (line[0:3] == 'ADD'):
            line = line.replace("ADD", "")
            line = line.split(',')
            op = "100"
            rx = format(int(line[0]), "02b")
            ry = format(int(line[1]), "02b")
            output = op + rx + ry
        
        elif (line[0:4] == 'INIT'):
            line = line.replace("INIT", "")
            line = line.split(',')
            
            op = "101"
            rx = format(int(line[0]), "02b")
            ry = format(int(line[1]), "02b")
            output = op + rx + ry
        
        elif (line[0:3] == 'XOR'):
            line = line.replace("XOR", "")
            line = line.split(',')
            
            op = "0001"
            rx = format(int(line[0]), "01b")
            rx = rx[0]
            ry = format(int(line[1]), "02b")
            
            output = op + rx + ry
        elif (line[0:3] == 'JIF'):
            line = line.replace("JIF", "")
            line = line.split(' ')
            op = "010"
            const = TwosComplement(int(line[0]), 4)
            const = format(const, "04b")
            
            output = op + const
        elif (line[0:5] == 'CNTR2'):
            line = line.replace("CNTR2", "")
            op = "0001"
            output = op + "000" 
        
        elif (line[0:5] == 'SUBR0'):
            line = line.replace("SUBR0", "")
            op = "0000"
            ry = format(int(line[0]), "02b")
            output = op + '0' + ry
        
        elif (line[0:3] == 'HLT'):
            line = line.replace("HLT", "")
            
            op = "000"
            
            output = op + "00" + "00" 
        numOnes = output.count("1")
        if ((numOnes % 2) == 0 and output != ""):
            output = '0' + output
        elif (output != ""):
            output = '1' + output
        if (output != ""):
            output_file.write(output + "\n")
            output = ""
    
    
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