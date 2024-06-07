import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('get fact restored.csv')
df2 = pd.read_csv('get plan restored.csv')

plt.figure(layout='constrained')
data = pd.DataFrame(columns=['data', 'Сиб'])
data['data'] = df['data']
data['Сиб'] = df['Сиб']
print(data)
plt.plot(df['data'], df['Сиб'])
plt.plot(df['data'], df2['Сиб'])
plt.show()