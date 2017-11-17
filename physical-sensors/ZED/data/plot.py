import matplotlib.pyplot as plt
import sys

values = []

with open(sys.argv[1]) as f:
    i = 0
    for l in f:
        if i == 0:
            i += 1
            continue

        l = l.strip()
        values.append(float(l))

print values

n, bins, patches = plt.hist(values, 50, normed=1, facecolor='green', alpha=0.75)

plt.xlabel("Depth (m)")
plt.ylabel("Probability")

plt.grid(True)

plt.savefig(sys.argv[1]+".png")

