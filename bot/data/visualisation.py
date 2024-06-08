import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


region = 'Сиб'

df = pd.read_csv('send fact restored.csv')
df2 = pd.read_csv('send plan restored.csv')

data = pd.DataFrame(columns=['data', region])
data['data'] = df['data']
data[region] = df[region]

fig, ax = plt.subplots(figsize=(5, 3))
fig.subplots_adjust(bottom=0.15, left=0.2)
ax.plot(df['data'], df[region], label='fact')
ax.plot(df['data'], df2[region], label='plan')
ax.set_xlabel('Data')
ax.set_ylabel('Amount of items')
ax.legend()


plt.show()
