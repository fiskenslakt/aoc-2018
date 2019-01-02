with open('clue.txt') as f:
    freq_changes = f.read().splitlines()

freqs = set()
cur_freq = 0
i = 0

while cur_freq not in freqs:
    freqs.add(cur_freq)
    cur_freq += int(freq_changes[i%len(freq_changes)])
    i += 1

print(cur_freq)
