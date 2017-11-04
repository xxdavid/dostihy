#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

rank = {}

with open("./stats.txt") as f:
    lines = f.readlines()

lines = [x.strip() for x in lines]

combinations = int(lines.pop(0))
set_length = int(lines.pop(0))
games_of_one_player = int(lines.pop(0))
lines.pop(0)  # blank newline

ranks = []

for line in lines:
    line_parts = line.split(" ")
    ranks.append((line_parts[0], int(line_parts[1]) / int(line_parts[2]) * 100))

ranks.sort(key=lambda x: x[1], reverse=True)

[names, percentage] = list(zip(*ranks))

fig, ax = plt.subplots()
ind = np.arange(len(names))  # compute y positions
width = .8
ax.bar(ind, percentage, width=width)
plt.xticks(ind - width / 2, names, rotation=70)
plt.xlabel("Strategies")
plt.ylabel("Won games [%]")
plt.title(f"Ranks in a tournament of {combinations * set_length} games ({combinations} combinations)")
plt.tight_layout()
plt.show()
