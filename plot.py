#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

rank = {}

with open("./stats.txt") as f:
    lines = f.readlines()

lines = [x.strip() for x in lines]

names = []
ranks = []

for line in lines:
    line_parts = line.split(" ")
    names.append(line_parts[0])
    ranks.append(line_parts[1])

print(names, ranks)


fig, ax = plt.subplots()
height = 0.75
ind = np.arange(len(ranks))
ax.barh(ind, ranks, height, color="blue")
ax.set_yticks(ind)
ax.set_yticklabels(names, minor=False)
plt.tight_layout()
plt.gca().invert_yaxis()
plt.show()
