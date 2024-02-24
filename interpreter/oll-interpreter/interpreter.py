import sys

# read arguments
program_filepath = sys.argv[1]

"""
Tokenize Program
"""

# read file lines
program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []
token_counter = 0
label_tracker = {}
for line in program_lines:
    tokens = line.split(" ")
    opcode = tokens[0]
    if opcode == "": # empty line
        continue 
    if opcode.endswith(":"): # if is label
        label_tracker[opcode[:-1]] = token_counter
        continue

    program.append(opcode) # store opcode
    token_counter += 1

    if opcode == "PUSH":
        program.append(int(tokens[1]))
    elif opcode == "PRINT":
        string_literal = ' '.join(tokens[1:])[1:-1]
        program.append(string_literal)
    elif opcode == "JUMP.EQ.0":
        program.append(tokens[1])
    elif opcode == "JUMP.GT.0":
        program.append(tokens[1])
    token_counter += 1

print(program)

"""
Interpret Program
"""

class Stack:

    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp = -1

    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        num = self.buf[self.sp]
        self.sp -= 1
        return num
    
    def top(self):
        return self.buf[self.sp]
    
pc = 0
stack = Stack(256)

while program[pc] != "HALT":
    opcode = program[pc]
    pc += 1
    if opcode == "PUSH":
        number = program[pc]
        pc += 1
        stack.push(number)
    elif opcode == "POP":
        stack.pop()
    elif opcode == "ADD":
        a = stack.pop()
        b = stack.pop()
        stack.push(a+b)
    elif opcode == "SUB":
        a = stack.pop()
        b = stack.pop()
        stack.push(b-a)
    elif opcode == "PRINT":
        string_literal = program[pc]
        pc += 1
        print(string_literal)
    elif opcode == "READ":
        num = int(input())
        stack.push(num)
    elif opcode == "JUMP.EQ.0":
        num = stack.top()
        if num == 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    elif opcode == "JUMP.GT.0":
        num = stack.top()
        if num > 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1