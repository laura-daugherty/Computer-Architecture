"""CPU functionality."""

import sys
LDI = "10000010"
PRN = "01000111"
HLT = "00000001"
MUL = "10100010"
ADD = "10100000"
PUSH = "01000101"
POP = "01000110"
CALL = "01010000"
RET = "00010001"
JMP = "01010100"
CMP = "10100111"
JEQ = "01010101"
JNE = "01010110"
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.fl = "00000000"


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

        # For now, we've just hardcoded a program:
        # address = 0
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
            # print(self.reg)
        #elif op == "SUB": etc

        elif op == MUL:
            print("multiplying in ALU")
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == CMP:
            print("CMP in ALU")
            # Compare the values in two registers.
            # * If they are equal,
            if self.reg[reg_a] == self.reg[reg_b]:
            #   set the Equal `E` flag to 1, 
                self.fl = "00000001"
                self.pc +=3
                print("self.fl", self.fl)
            # * If registerA is less than registerB, 
            #   set the Less-than `L` flag to 1,
            # otherwise 
            #   set it to 0.
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = "00000100"
                self.pc +=3
                print("self.fl", self.fl)

#             * If registerA is greater than registerB, 
#                 set the Greater-than `G` flag
#               to 1, otherwise set it to 0
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = "00000010"
                self.pc +=3
                print("self.fl", self.fl)

            else:
                self.fl = "00000000"
                self.pc +=3
                print("self.fl", self.fl)

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
            if ir == LDI:
                print("writing")
                self.raw_write(operand_b, operand_a)
                self.pc += 3
            elif ir == PRN:
                print("printing")
                # print("opA", operand_a)
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == PUSH:
                print("pushing")
                # print("register", self.reg)
                # print("ram", self.ram)
                reg = self.ram[self.pc + 1]
                # print("push reg", reg)
                val = self.reg[int(reg)]
                # print("push val", val)
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = val
                self.pc +=2
            elif ir == POP:
                print("popping")
                # print("register", self.reg)
                # print("ram", self.ram)
                reg = self.ram[self.pc + 1]
                # print("reg", reg)
                val = self.ram[self.reg[self.sp]]
                # print("val", val)
                # print("int reg", int(reg, 2))
                self.reg[int(reg, 2) ] = val
                self.reg[self.sp] += 1
                self.pc += 2
            elif ir == CALL:
                print("calling")
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[int(reg, 2)]
            elif ir == CMP:
                print("CMP")
                self.alu(ir, operand_a, operand_b)
            elif ir == JMP:
                print("jumping")
                # self.reg[self.sp] -= 1
                # self.ram[self.reg[self.sp]] = self.pc + 2
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[int(reg, 2)]
            elif ir == JEQ:
                # print(self.fl[-1])
                print("JEQ")
                if self.fl[-1] == "1":
                    reg = self.ram[self.pc + 1]
                    # print(reg)
                    self.pc = self.reg[int(reg, 2)]
                    # print(self.reg)
                else:
                    self.pc += 2

                # print("JEQ register")
                # If `equal` flag is set (true), 
                    # jump to the address stored in the given register.
            elif ir == JNE:
                print("JNE register")

                if self.fl[-1] == "0":
                    reg = self.ram[self.pc + 1]
                    self.pc = self.reg[int(reg, 2)]
                    # print(self.reg)
                else:
                    self.pc += 2
                #If `E` flag is clear (false, 0), 
                    # jump to the address stored in the given register.

            elif ir == RET:
                print("returning")
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
            elif ir == MUL:
                self.alu(ir, operand_a, operand_b)
            elif ir == ADD:
                self.alu(ir, operand_a, operand_b)
            elif ir == HLT:
                print("halting")
                sys.exit(1)
