"""CPU functionality."""

import sys
from opcode import *
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.fl = "00000000"
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE

    
    def handle_LDI(self, ir, operand_a, operand_b):
        print("writing")
        self.raw_write(operand_b, operand_a)
        self.calculate_pc(ir)
    def handle_PRN(self, ir, operand_a):
        print(self.reg[operand_a])
        self.calculate_pc(ir)
    def handle_HLT(self):
        sys.exit(1)
    def handle_MUL(self, op, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]
        self.calculate_pc(op)    
    def handle_ADD(self, op, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]
        self.calculate_pc(op)    
    def handle_PUSH(self, ir):
        # print("register", self.reg)
        # print("ram", self.ram)
        reg = self.ram[self.pc + 1]
        # print("push reg", reg)
        val = self.reg[int(reg)]
        # print("push val", val)
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = val
        self.calculate_pc(ir)
    def handle_POP(self, ir):
        # print("register", self.reg)
        # print("ram", self.ram)
        reg = self.ram[self.pc + 1]
        # print("reg", reg)
        val = self.ram[self.reg[self.sp]]
        # print("val", val)
        # print("int reg", int(reg, 2))
        self.reg[int(reg, 2) ] = val
        self.reg[self.sp] += 1
        self.calculate_pc(ir)
    def handle_CALL(self):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        reg = self.ram[self.pc + 1]
        self.pc = self.reg[int(reg, 2)]    
    def handle_RET(self):
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1    
    def handle_JMP(self):
        reg = self.ram[self.pc + 1]
        self.pc = self.reg[int(reg, 2)]
    def handle_CMP(self, op, reg_a, reg_b):
        # Compare the values in two registers.
        # * If they are equal,
        if self.reg[reg_a] == self.reg[reg_b]:
        #   set the Equal `E` flag to 1, 
            self.fl = "00000001"
            self.calculate_pc(op)
            print("self.fl", self.fl)
        # * If registerA is less than registerB, 
        #   set the Less-than `L` flag to 1,
        # otherwise 
        #   set it to 0.
        elif self.reg[reg_a] < self.reg[reg_b]:
            self.fl = "00000100"
            self.calculate_pc(op)
            print("self.fl", self.fl)
#             * If registerA is greater than registerB, 
#                 set the Greater-than `G` flag
#               to 1, otherwise set it to 0
        elif self.reg[reg_a] > self.reg[reg_b]:
            self.fl = "00000010"
            self.calculate_pc(op)
            print("self.fl", self.fl)
        else:
            self.fl = "00000000"
            self.calculate_pc(op)
            print("self.fl", self.fl)
    def handle_JEQ(self, ir):
        if self.fl[-1] == "1":
            reg = self.ram[self.pc + 1]
            # print(reg)
            self.pc = self.reg[int(reg, 2)]
            # print(self.reg)
        else:
            self.calculate_pc(ir)    
    def handle_JNE(self, ir):
        if self.fl[-1] == "0":
            reg = self.ram[self.pc + 1]
            self.pc = self.reg[int(reg, 2)]
            # print(self.reg)
        else:
            self.calculate_pc(ir)
        #If `E` flag is clear (false, 0), 
            # jump to the address stored in the given register.

    def load(self, filename):
    # def load(self):
        # """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                #read all the lines
                for line in f:
                    #parse out comments
                    comment_split = line.strip().split("#")
                    value = comment_split[0].strip()
                    if value == "":
                        continue
                    # print("value", value)
                    num = value
                    self.ram[address] = num
                    address += 1
            # print(self.ram)
        except FileNotFoundError:
            print("File not Found")
            sys.exit(2)

    def calculate_pc(self, op):
        self.pc += (int(op, 2) >> 6) + 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == ADD:
            self.branchtable[op](op, reg_a, reg_b)
        elif op == MUL:
            print("multiplying in ALU")
            self.branchtable[op](op, reg_a, reg_b)
        elif op == CMP:
            print("CMP in ALU")
            self.branchtable[op](op, reg_a, reg_b)
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

        print()

    def ram_read(self, mar):
        return self.ram[mar]

    def raw_write(self, mdr, mar):
        self.reg[mar] = mdr

    def run(self):
        """Run the CPU."""
        while True:
            # print("loop ram", self.ram)
            # print("pc", self.pc)
            ir = self.ram[self.pc]
            # print("ir", ir)
            # print("ir type", type(ir))
            # print("LDI", LDI)
            # print("LDI type", type(LDI))
            operand_a = int(str(self.ram_read(self.pc + 1)), 2)
            operand_b = int(str(self.ram_read(self.pc + 2)), 2)
            print("op A", operand_a)
            print("op B", operand_b)
            if ir == LDI:
                print("writing")
                self.branchtable[ir](ir, operand_a, operand_b)
            elif ir == PRN:
                print("printing")
                self.branchtable[ir](ir, operand_a)
            elif ir == PUSH:
                print("pushing")
                self.branchtable[ir](ir)
            elif ir == POP:
                print("popping")
                self.branchtable[ir](ir)
            elif ir == CALL:
                print("calling")
                self.branchtable[ir]()
            elif ir == CMP:
                print("CMP")
                self.alu(ir, operand_a, operand_b)
            elif ir == JMP:
                print("jumping")
                self.branchtable[ir]()
            elif ir == JEQ:
                print("JEQ")
                self.branchtable[ir](ir)
            elif ir == JNE:
                print("JNE register")
                self.branchtable[ir](ir)
            elif ir == RET:
                print("returning")
                self.branchtable[ir]()
            elif ir == MUL:
                self.alu(ir, operand_a, operand_b)
            elif ir == ADD:
                self.alu(ir, operand_a, operand_b)
            elif ir == HLT:
                print("halting")
                self.branchtable[ir]()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: file.py filename", file=sys.stderr)
        sys.exit(1)
    cpu = CPU()
    cpu.load(sys.argv[1])
    cpu.run()