import pandas as pd
from pandas import read_csv
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt

region = 'Центр'

def prepareData(data, res):

    global region
    data2 = pd.DataFrame(columns=['year', 'month', region, 'mean3'])
    data2['year'] = data['year']
    data2['month'] = data['month']
    data2[region] = data[region]

    for index, row in data2.iterrows():
        if index > 0 and index < 59:
            data2.at[index, 'mean3'] = (data2.at[index - 1, region] + data2.at[index, region] + data2.at[index + 1, region]) / 3
        elif index == 0:
            data2.at[index, 'mean3'] = (data2.at[index, region] + data2.at[index + 1, region]) / 2
        else:
            data2.at[index, 'mean3'] = (data2.at[index, region] + data2.at[index - 1, region]) / 2

    test_index = 50

    # разбиваем весь датасет на тренировочную и тестовую выборку
    X_train = data2.loc[:test_index]
    y_train = res.loc[:test_index][region]
    X_test = data2
    y_test = res[region]

    return X_train, X_test, y_train, y_test

dataset = read_csv('../get plan restored.csv', delimiter=',')
dataset2 = read_csv('../get fact restored.csv', delimiter=',')

X_train, X_test, y_train, y_test = prepareData(dataset, dataset2)
lr = KNeighborsRegressor()
lr.fit(X_train, y_train)
prediction = lr.predict(X_test)

plt.figure(figsize=(15, 7))
plt.plot(dataset['data'], dataset2[region], prediction)
# plt.show()

x = pd.DataFrame(columns=['year', 'month', region, 'mean3'])
amount = input().split()
for i in range(len(amount)):
    mean = 0
    if i == 0 and len(amount) > 1:
        mean = (int(amount[i]) + int(amount[i + 1])) / 2
    elif i == 0:
        mean = int(amount[i])
    elif i == len(amount) - 1:
        mean = (int(amount[i]) + int(amount[i - 1])) / 2
    else:
        mean = (int(amount[i - 1]) + int(amount[i]) + int(amount[i + 1])) / 3
    x.loc[len(x.index)] = [datetime.date.today().year, datetime.date.today().month + i + 1, int(amount[i]), mean]

count = 60
data = [count - 1]
for i in range(len(amount)):
    data += [count + i]

prediction = lr.predict(x)
res = [dataset2.at[len(dataset2.index) - 1, region]]
for i in range(len(prediction)):
    res += [prediction[i]]

# plt.figure(figsize=(15, 7))
plt.plot(data, res)
plt.show()