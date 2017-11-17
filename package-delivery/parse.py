import sys
import pandas as pd

columns = ['noise', 'time', 'replans', 'failed', 'plan_time', 'spin_time', 'collisions']
df = pd.DataFrame(columns=columns)

noise = ""
start = 0
end = 0
replans = 0
collisions = 0
failed = None
start_planning_time = 0
total_planning_time = 0
start_spinning_time = 0
total_spinning_time = 0

def reset():
    global noise, start, end, replans, failed, collisions, start_planning_time, total_planning_time, start_spinning_time, total_spinning_time
    noise = ""
    start = 0
    end = 0
    replans = 0
    collisions = 0
    failed = None
    start_planning_time = 0
    total_planning_time = 0
    start_spinning_time = 0
    total_spinning_time = 0

reset()

with open(sys.argv[1]) as f:
    for line in f:
        words = line.strip().split()

        if "New noise!" in line:
            if failed is None:
                failed = True

            if noise != "":
                df = df.append(pd.DataFrame({'noise':noise, 'time':end-start, 'replans':replans, 'failed':failed, 'plan_time':total_planning_time, 'spin_time':total_spinning_time, 'collisions':collisions}, index=[0]))

            reset()

        if '[ INFO]' in line or '[ WARN]' in line or '[ ERROR]' in line:
            if start == 0:
                start = float(words[2][1:][:-2])
            end = float(words[2][1:][:-2])

        if "Std dev:" in line:
           noise = words[-1]
        elif "Obstacle appeared on trajectory" in line:
            replans += 1
        elif "Collision count" in line:
            collisions += 1
        elif "Failed to call service" in line:
            failed = True
        elif "Delivered the package and returned!" in line and failed != True:
            failed = False
        elif ("Spinning around" in line or "Scanning around" in line):
            start_spinning_time = float(words[2][1:][:-2])
        elif "Distance to target" in line:
            total_spinning_time += float(words[2][1:][:-2]) - start_spinning_time
            start_planning_time = float(words[2][1:][:-2])
        elif "Received trajectory" in line:
            total_planning_time += float(words[2][1:][:-2]) - start_planning_time


# Now average out results
# columns = ['noise', 'time', 'replans', 'failed', 'plan_time', 'spin_time']
df2 = pd.DataFrame(columns=columns)
for n in df.noise.unique():
    df3 = df.loc[df['noise'] == n]
    df4 = df3.loc[df3['failed'] == False]

    new_row = dict()

    new_row['noise'] = n
    new_row['time'] = df4['time'].mean()
    new_row['replans'] = df4['replans'].mean()
    new_row['plan_time'] = df4['plan_time'].mean()
    new_row['spin_time'] = df4['spin_time'].mean()
    new_row['collisions'] = df3['collisions'].mean()

    fails = len(df3) - len(df4)
    successes = len(df4)
    new_row['failed'] = float(fails) * 100 / (successes + fails)

    df2 = df2.append(pd.DataFrame(new_row, index=[0]))

df2.to_csv(sys.argv[2], index=False)

df.to_csv("scatter.csv", index=False)

