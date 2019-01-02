import re
import heapq
from collections import deque


class Workers:
    seconds = 0
    completed = []
    still_working = set()

    def __init__(self, elves):
        self.elves = []
        for elf in range(elves):
            self.elves.append([])

    def available_elves(self):
        return len([elf for elf in self.elves if not elf])

    def get_idle_elf(self):
        return self.elves.index([])

    def get_working_elves_index(self):
        return [self.elves.index(elf) for elf in self.elves if elf]

    def get_working_elves(self):
        return [elf for elf in self.elves if elf]

    def assign_elf(self, letter):
        self.still_working.add(letter)
        idle_elf = self.get_idle_elf()
        self.elves[idle_elf] = [letter] * (ord(letter) - 4)

    def pass_time(self):
        duration = len(min(self.get_working_elves(), key=len))
        elves = [(idx,elf[0]) for idx, elf in enumerate(self.elves) if len(elf) == duration]
        for elf, letter in elves:
            self.elves[elf].clear()
            self.still_working.remove(letter)
            self.completed.append(letter)

        self.seconds += duration

        for elf in self.get_working_elves_index():
            letter = self.elves[elf][0]
            for _ in range(duration):
                if self.elves[elf]:
                    self.elves[elf].pop()
                else:
                    self.completed.append(letter)
                    self.still_working.remove(letter)


def unsatisfied_prereq(graph, _next, done):
    for letter in graph.keys():
        if _next in graph.get(letter,[]) and letter not in done:
            return True


with open('clue.txt') as f:
    steps = f.read().splitlines()

step_graph = {}
prereqs = set()
reqs = set()
step_pattern = r'Step (\w).+step (\w)'

for step in steps:
    inst1, inst2 = re.match(step_pattern, step).groups()
    if inst2 not in reqs:
        reqs.add(inst2)
    if inst1 not in prereqs:
        prereqs.add(inst1)
        step_graph[inst1] = []

    step_graph[inst1].append(inst2)
    step_graph[inst1].sort()

available = list(prereqs - reqs)
heapq.heapify(available)
order = []

while available:
    _next = heapq.heappop(available)

    if unsatisfied_prereq(step_graph, _next, order):
        continue
    else:
        order.append(_next)

        for letter in order:
            if letter in step_graph:
                for newly_available in step_graph[letter]:
                    if newly_available in order or newly_available in available:
                        continue
                    else:
                        heapq.heappush(available, newly_available)

print('Part 1:',''.join(list(order)))

workers = Workers(5)
jobs = deque(sorted(list(prereqs - reqs), reverse=True))

while jobs:
    while any(not unsatisfied_prereq(step_graph, job, workers.completed) for job in jobs):
        if workers.available_elves():
            if unsatisfied_prereq(step_graph, jobs[-1], workers.completed):
                jobs.rotate()
            else:
                workers.assign_elf(jobs.pop())
        else:
            break

    if workers.still_working:
        workers.pass_time()

    for letter in workers.completed:
        for job in step_graph.get(letter, []):
            if job not in jobs \
            and job not in workers.completed \
            and job not in workers.still_working:
                jobs.appendleft(job)

print(f'Part 2: {workers.seconds}')
