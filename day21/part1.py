class CPU:
    def __init__(self, register, ip, instructions):
        self.register = register
        self._ip = ip
        self.instructions = instructions

    @property
    def op(self):
        return getattr(self, self.instruction[0])

    @property
    def A(self):
        return int(self.instruction[1])

    @property
    def B(self):
        return int(self.instruction[2])

    @property
    def C(self):
        return int(self.instruction[3])

    @property
    def ip(self):
        return self.register[self._ip]

    @property
    def instruction(self):
        return self.instructions[self.ip]

    @property
    def halt(self):
        if 0 <= self.register[self._ip] < len(self.instructions):
            return False
        else:
            return True

    def inc_pointer(self):
        self.register[self._ip] += 1

    def addr(self):
        self.register[self.C] = self.register[self.A] + self.register[self.B]

    def addi(self):
        self.register[self.C] = self.register[self.A] + self.B

    def mulr(self):
        self.register[self.C] = self.register[self.A] * self.register[self.B]

    def muli(self):
        self.register[self.C] = self.register[self.A] * self.B

    def banr(self):
        self.register[self.C] = self.register[self.A] & self.register[self.B]

    def bani(self):
        self.register[self.C] = self.register[self.A] & self.B

    def borr(self):
        self.register[self.C] = self.register[self.A] | self.register[self.B]

    def bori(self):
        self.register[self.C] = self.register[self.A] | self.B

    def setr(self):
        self.register[self.C] = self.register[self.A]

    def seti(self):
        self.register[self.C] = self.A

    def gtir(self):
        if self.A > self.register[self.B]:
            self.register[self.C] = 1
        else:
            self.register[self.C] = 0

    def gtri(self):
        if self.register[self.A] > self.B:
            self.register[self.C] = 1
        else:
            self.register[self.C] = 0

    def gtrr(self):
        if self.register[self.A] > self.register[self.B]:
            self.register[self.C] = 1
        else:
            self.register[self.C] = 0

    def eqir(self):
        if self.A == self.register[self.B]:
            self.register[self.C] = 1
        else:
            self.register[self.C] = 0

    def eqri(self):
        if self.register[self.A] == self.B:
            self.register[self.C] = 1
        else:
            self.register[self.C] = 0

    def eqrr(self):
        if self.register[self.A] == self.register[self.B]:
            self.register[self.C] = 1
        else:
            self.register[self.C] = 0


with open('clue.txt') as f:
    ip = int(next(f).split()[1])
    ops = list(map(str.split, f.read().splitlines()))

register = [0]*6
cpu = CPU(register, ip, ops)

while not cpu.halt:
    cpu.op()
    cpu.inc_pointer()
    if cpu.register[4] == 28:
        print('Part 1:', cpu.register[3])
        break

register = [0]*6
cpu = CPU(register, ip, ops)
last = None
halts = set()

while not cpu.halt:
    cpu.op()
    cpu.inc_pointer()
    if cpu.register[4] == 28:
        if cpu.register[3] in halts:
            print('Part 2:',last)
            break
        else:
            halts.add(cpu.register[3])
            last = cpu.register[3]
