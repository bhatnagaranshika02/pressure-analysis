import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    'over': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'runs_scored': [5, 10, 8, 6, 7, 4, 3, 12, 2, 5],
    'wickets_lost': [0, 0, 1, 0, 0, 1, 0, 1, 1, 0]
}

targeted_score = 150
total_overs = 20

df = pd.DataFrame(data)

df['cumulative_runs'] = df['runs_scored'].cumsum()
df['cumulative_wickets'] = df['wickets_lost'].cumsum()
df['over_bowled'] = df['over']

df['current_run_rate'] = df['cumulative_runs'] / df['over_bowled']
df['required_run_rate'] = (targeted_score - df['cumulative_runs']) / (total_overs - df['over_bowled'])
df['required_run_rate'] = df['required_run_rate'].replace([np.inf, -np.inf], np.nan).fillna(0)

# Calculating pressure index
WICKET_WEIGHT = 10
RRR_WEIGHT = 2
CRR_WEIGHT = 1.5

df['pressure_index'] = (df['cumulative_wickets'] * WICKET_WEIGHT) + \
                       (df['required_run_rate'] * RRR_WEIGHT) - \
                       (df['current_run_rate'] * CRR_WEIGHT)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df['over'], df['pressure_index'], marker='o', color='darkred', label='Pressure Index')

# Annotate points
for i, row in df.iterrows():
    plt.text(row['over'], row['pressure_index'] + 1, f"{row['pressure_index']:.1f}", ha='center', fontsize=8)

plt.title("Pressure Index Over Time")
plt.xlabel("Over")
plt.ylabel("Pressure Index")
plt.xticks(df['over'])
plt.yticks(np.arange(int(df['pressure_index'].min()) - 5,
                     int(df['pressure_index'].max()) + 5, 5))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("pressure_index_graph.png")
plt.show()
