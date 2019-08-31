"""CPU functionality."""

import sys

# HLT = 0b00000001
# PRN = 0b01000111
# LDI = 0b10000010
# MUL = 0b10100010 
# POP = 0b01000110
# PUSH = 0b01000101
# RET = 0b00010001
# CALL = 0b01010000
# JMP = 0b01010100
# JNE = 0b01010110
# JEQ = 0b01010101

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[SP] = 0xF4
        self.hlt = False
        # self.inst_set_pc = False
        self.fl = None

        self.op_table = {}
        self.op_table[0b10000010] = self.op_ldi
        self.op_table[0b01000111] = self.op_prn
        self.op_table[0b00000001] = self.op_hlt
        self.op_table[0b01000101] = self.op_push
        self.op_table[0b01000110] = self.op_pop
        self.op_table[0b00010001] = self.op_ret
        self.op_table[0b01010000] = self.op_call
        self.op_table[0b01010100] = self.op_jmp
        self.op_table[0b01010101] = self.op_jeq
        self.op_table[0b01010110] = self.op_jne

        # self.ins = {
        #     # ADD: self.op_add,
        #     HLT: self.op_hlt,
        #     LDI: self.op_ldi,
        #     MUL: self.op_mul,
        #     PRN: self.op_prn,
        #     POP: self.op_pop,
        #     PUSH: self.op_push,
        #     RET: self.op_ret,
        #     CALL: self.op_call,
        #     JMP: self.op_jmp,
        #     JNE: self.op_jne,
        #     JEQ: self.op_jeq

        # }


    def ram_read(self, pc_address):
        return self.ram[pc_address]

    def ram_write(self, value, pc_address):
        self.ram[value] = pc_address

    
    # def op_add(self, reg1, reg2):
    #     self.reg[reg1] += self.reg[reg2]

    def op_hlt(self, operand_a, operand_b):
        self.hlt = True

    def op_ldi(self, addr, value):
        self.reg[addr] = value

    def op_mul(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)

    def op_prn(self, addr, operand_b):
        print(self.reg[addr])

    def op_pop(self, addr, operand_b):
        value = self.ram_read(self.reg[SP])
        self.ram_write(self.reg[SP], 0)
        self.reg[addr] = value
        self.reg[SP] += 1
    def op_push(self, addr, operand_b):
        self.reg[SP] -= 1
        value = self.reg[addr]
        self.ram_write(self.reg[SP], value)
    
    def op_ret(self):
        address = self.ram[self.reg[SP]]
        self.pc = address
        self.reg[SP] += 1
 
    def op_call(self, operand_a):
        self.reg[SP] -= 1
        address = self.pc + 2
        self.ram[self.reg[SP]] = address
        sub_address = self.ram[operand_a]
        self.reg[SP] = sub_address
    
    def op_jmp(self, operand_a): 
        self.pc = self.reg[operand_a]

    def op_jne(self, operand_a):
        if self.fl != 0b00000010:
            self.pc = self.reg[operand_a]
        else: 
            self.pc += 2

    def op_jeq(self, operand_a):
        if self.fl == 0b00000010:
            self.pc = self.reg[operand_a]
        else: 
            self.pc += 2

        def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('Usage: using file <filename>', file = sys.stderr)
            sys.exit(1)
        try:
            # sys.argv is a list in Python, which contains the command-line arguments passed to the script.
            with open(sys.argv[1]) as f:  # open a file
                for line in f:
                    if line[0].startswith('0') or line[0].startswith('1'):
                        # search first part of instruction
                        num = line.split('#')[0]
                        num = num.strip()  # remove empty space
                        # convert binary to int and store in a memory(RAM)
                        self.ram[address] = int(num, 2)
                        address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} Not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        MUL = 0b10100010
        ADD = 0b10100000
        SUB = 0b10100001
        DIV = 0b10100011
        XOR = 0b10101011
        SHR = 0b10101101
        SHL = 0b10101100
        CMP = 0b10100111


        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        
        elif op == "XOR":
            xor = self.reg[reg_a]^self.reg[reg_b]
            self.reg[reg_b] = xor

        elif op == "SHR":
            shr = self.reg[reg_a]
            right = shr >> self.reg[reg_b]
            self.reg[reg_a] = right
        
        elif op == "SHL":
            shl = self.reg[reg_a]
            left = shl << self.reg[reg_b]
            self.reg[reg_a] = left
        
        elif op == "CMP":
            a = self.reg[reg_a]
            b = self.reg[reg_b]
            if a == b:
                self.fl = 0b00000010
            elif a < b:
                self.fl = 0b00000100
            elif a > b: 
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
            
    def run(self):
        ir = self.ram[self.pc]
        """Run the CPU."""
        while not self.hlt:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # int_size = (ir >> 6) 
            # self.inst_set_pc = ((ir >> 4) & 0b1) == 1
        

            cpu_op = (ir & 0b11000000) >> 6
            alu_op = (ir & 0b00100000) >> 5

            if ir == self.op_call:
                self.op_table[ir](operand_a)
                continue

            elif ir == self.op_ret:
                self.op_table[ir]()
                continue
            
            if alu_op:
                self.alu(ir, operand_a, operand_b)
            elif cpu_op == 2:
                self.op_table[ir](operand_a, operand_b)
            elif cpu_op == 1:
                self.op_table[ir](operand_a)
            elif cpu_op == 0:
                self.op_table[ir]()
            else:
                self.op_hlt()
#     # Code to test the Sprint Challenge
# #
# # Expected output:
# # 1
# # 4
# # 5

# 10000010 # LDI R0,10
# 00000000
# 00001010
# 10000010 # LDI R1,20
# 00000001
# 00010100
# 10000010 # LDI R2,TEST1
# 00000010
# 00010011
# 10100111 # CMP R0,R1
# 00000000
# 00000001
# 01010101 # JEQ R2
# 00000010
# 10000010 # LDI R3,1
# 00000011
# 00000001
# 01000111 # PRN R3
# 00000011
# # TEST1 (address 19):
# 10000010 # LDI R2,TEST2
# 00000010
# 00100000
# 10100111 # CMP R0,R1
# 00000000
# 00000001
# 01010110 # JNE R2
# 00000010
# 10000010 # LDI R3,2
# 00000011
# 00000010
# 01000111 # PRN R3
# 00000011
# # TEST2 (address 32):
# 10000010 # LDI R1,10
# 00000001
# 00001010
# 10000010 # LDI R2,TEST3
# 00000010
# 00110000
# 10100111 # CMP R0,R1
# 00000000
# 00000001
# 01010101 # JEQ R2
# 00000010
# 10000010 # LDI R3,3
# 00000011
# 00000011
# 01000111 # PRN R3
# 00000011
# # TEST3 (address 48):
# 10000010 # LDI R2,TEST4
# 00000010
# 00111101
# 10100111 # CMP R0,R1
# 00000000
# 00000001
# 01010110 # JNE R2
# 00000010
# 10000010 # LDI R3,4
# 00000011
# 00000100
# 01000111 # PRN R3
# 00000011
# # TEST4 (address 61):
# 10000010 # LDI R3,5
# 00000011
# 00000101
# 01000111 # PRN R3
# 00000011
# 10000010 # LDI R2,TEST5
# 00000010
# 01001001
# 01010100 # JMP R2
# 00000010
# 01000111 # PRN R3
# 00000011
# # TEST5 (address 73):
# 00000001 # HLT