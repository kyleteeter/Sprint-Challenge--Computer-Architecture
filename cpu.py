"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010 
POP = 0b01000110
PUSH = 0b01000101
RET = 0b00010001
CALL = 0b01010000
JMP = 0b01010100

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
        self.inst_set_pc = False
        self.fl = None

        self.ins = {
            # ADD: self.op_add,
            HLT: self.op_hlt,
            LDI: self.op_ldi,
            MUL: self.op_mul,
            PRN: self.op_prn,
            POP: self.op_pop,
            PUSH: self.op_push,
            RET: self.op_ret,
            CALL: self.op_call,
            JMP: self.op_jmp,

        }




    def load(self, filename):
        """Load a program into memory."""

        address = 0

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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def ram_read(self, pc_address):
        return self.ram[pc_address]

    def ram_write(self, value, pc_address):
        self.ram[value] = pc_address

    def run(self):
        """Run the CPU."""
        while not self.hlt:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            int_size = (ir >> 6) 
            self.inst_set_pc = ((ir >> 4) & 0b1) == 1
        

            if ir in self.ins:
                self.ins[ir](operand_a, operand_b)
            else:
                print('error: command not found')
            
            if not self.inst_set_pc:
                self.pc += int_size + 1

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