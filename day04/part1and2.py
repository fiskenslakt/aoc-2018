import re
from collections import Counter
from operator import itemgetter
from datetime import datetime

with open('linux.txt') as f:
    raw_logs = f.read().splitlines()

log_pattern = r'(\d+)-(\d+)-(\d+) (\d+):(\d+)] (.+)+'
id_pattern = r'(\d+)'

logs = []
for line in raw_logs:
    *dt, log = re.findall(log_pattern, line)[0]
    log_date = datetime(*list(map(int,dt)))
    logs.append((log_date, log))

guards = {}
guard_stack = []

for log_date, log in sorted(logs):
    if 'Guard' in log:
        guard_id = re.findall(id_pattern, log)[0]
        guard_stack = [guard_id]

        if guard_id not in guards:
            guards[guard_id] = []

    elif 'falls' in log:
        guard_stack.append(log_date)

    elif 'wakes' in log:
        guard_id, start_sleep = guard_stack
        minutes = (log_date - start_sleep).seconds // 60

        for minute in range(start_sleep.minute, start_sleep.minute + minutes):
            guards[guard_id].append(minute)

        guard_stack.pop()

strategy_1_guard = max(guards, key=lambda ID: len(guards[ID]))
strategy_1_minute = Counter(guards[strategy_1_guard]).most_common(1)[0][0]

print(f'Part 1: {int(strategy_1_guard) * strategy_1_minute}')

strategy_2_guard =  max([(g, Counter(m).most_common(1)[0][1]) for g, m in guards.items() if m], key=itemgetter(1))[0]
strategy_2_minute = Counter(guards[strategy_2_guard]).most_common(1)[0][0]

print(f'Part 2: {int(strategy_2_guard) * strategy_2_minute}')
