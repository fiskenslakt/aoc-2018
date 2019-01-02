import re


class CPU:
    def __init__(self, register, opcode, register_out=None):
        self.register = [int(r) for r in register]
        self.opcode = [int(o) for o in opcode]
        if register_out:
            self.register_out = [int(r) for r in register_out]

        self.A = self.opcode[1]
        self.B = self.opcode[2]
        self.C = self.opcode[3]

    def addr(self):
        register = self.register.copy()
        register[self.C] = register[self.A] + register[self.B]
        return register

    def addi(self):
        register = self.register.copy()
        register[self.C] = register[self.A] + self.B
        return register

    def mulr(self):
        register = self.register.copy()
        register[self.C] = register[self.A] * register[self.B]
        return register

    def muli(self):
        register = self.register.copy()
        register[self.C] = register[self.A] * self.B
        return register

    def banr(self):
        register = self.register.copy()
        register[self.C] = register[self.A] & register[self.B]
        return register

    def bani(self):
        register = self.register.copy()
        register[self.C] = register[self.A] & self.B
        return register

    def borr(self):
        register = self.register.copy()
        register[self.C] = register[self.A] | register[self.B]
        return register

    def bori(self):
        register = self.register.copy()
        register[self.C] = register[self.A] | self.B
        return register

    def setr(self):
        register = self.register.copy()
        register[self.C] = register[self.A]
        return register

    def seti(self):
        register = self.register.copy()
        register[self.C] = self.A
        return register

    def gtir(self):
        register = self.register.copy()
        if self.A > register[self.B]:
            register[self.C] = 1
        else:
            register[self.C] = 0
        return register

    def gtri(self):
        register = self.register.copy()
        if register[self.A] > self.B:
            register[self.C] = 1
        else:
            register[self.C] = 0
        return register

    def gtrr(self):
        register = self.register.copy()
        if register[self.A] > register[self.B]:
            register[self.C] = 1
        else:
            register[self.C] = 0
        return register

    def eqir(self):
        register = self.register.copy()
        if self.A == register[self.B]:
            register[self.C] = 1
        else:
            register[self.C] = 0
        return register

    def eqri(self):
        register = self.register.copy()
        if register[self.A] == self.B:
            register[self.C] = 1
        else:
            register[self.C] = 0
        return register

    def eqrr(self):
        register = self.register.copy()
        if register[self.A] == register[self.B]:
            register[self.C] = 1
        else:
            register[self.C] = 0
        return register

    def test_ops(self, tests):
        samples = 0
        for test in tests:
            if getattr(self,test)() == self.register_out:
                samples += 1

        return 1 if samples >= 3 else 0

with open('clue1.txt') as f:
    raw_data = f.read().splitlines()

before = []
opcodes = []
after = []

for line in raw_data:
    if line.startswith('Before'):
        before.append(re.findall(r'(\d+)', line))
    elif line.startswith('After'):
        after.append(re.findall(r'(\d+)', line))
    elif not line:
        continue
    else:
        opcodes.append(re.findall(r'(\d+)', line))

tests = [f for f in dir(CPU) if callable(getattr(CPU, f)) and not f.startswith("__") and not f.startswith('test')]
samples = 0

for op in zip(before, opcodes, after):
    cpu = CPU(*op)
    samples += cpu.test_ops(tests)

print(f'Part 1: {samples}')

f_to_op = {}

for test in tests:
    if test not in f_to_op:
        f_to_op[test] = set()

    for op in zip(before, opcodes, after):
        cpu = CPU(*op)
        op_num = op[1][0]
        f = getattr(CPU, test)
        if f(cpu) == cpu.register_out:
            f_to_op[test].add(op_num)

op_to_f = {}

while any(len(i)>1 for i in f_to_op.values()):
    for k, v in f_to_op.items():
        if len(v) == 1:
            v = v.pop()
            op_to_f[v] = k
            for i in f_to_op:
                f_to_op[i].discard(v)

with open('clue2.txt') as f:
    instructions_raw = f.read().splitlines()

instructions = []

for instruction in instructions_raw:
    instruction = re.findall(r'(\d+)', instruction)
    instructions.append(instruction)

register = ['0']*4

for instruction in instructions:
    cpu = CPU(register, instruction)
    f = op_to_f[instruction[0]]
    f = getattr(CPU, f)
    register = f(cpu)

print(f'Part 2: {register[0]}')
