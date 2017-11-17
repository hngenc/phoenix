import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv(sys.argv[1])
df2 = df.dropna()

plt.plot(df2['noise'], df2['time'])
plt.ylabel('Time to complete (s)')
plt.xlabel('Noise std dev (m)')
plt.savefig(sys.argv[2])
plt.close()

plt.plot(df2['noise'], df2['replans'])
plt.ylabel('Replans')
plt.xlabel('Noise std dev (m)')
plt.ylim(0, 5.0)
plt.savefig(sys.argv[3])
plt.close()

plt.plot(df['noise'], df['failed'])
plt.ylabel('Failure rate (%)')
plt.xlabel('Noise std dev (m)')
plt.ylim(0, 105)
plt.savefig(sys.argv[4])
plt.close()

plt.plot(df['noise'], df['collisions'])
plt.ylabel('Collisions')
plt.xlabel('Noise std dev (m)')
plt.ylim(0, 10)
plt.savefig(sys.argv[5])
plt.close()

# Stacked bar plots!
spin = df['spin_time']
plan = df['plan_time']
fly = df['time'] - df['spin_time'] - df['plan_time']
width = 0.8

p_spin = plt.bar(np.arange(len(df['noise'])), spin, width, color="blue")
p_plan = plt.bar(np.arange(len(df['noise'])), plan, width, bottom=spin, color="red")
p_fly = plt.bar(np.arange(len(df['noise'])), fly, width, bottom=spin+plan, color="green")
plt.xlabel('Noise std dev (m)')
plt.ylabel('Time (s)')
plt.legend((p_spin[0], p_plan[0], p_fly[0]), ('Spin', 'Plan', 'Fly'), loc="upper left")
# plt.xticks(df['noise'])

plt.savefig(sys.argv[6])

