import time
import numpy as np
from pandas import read_csv, DataFrame, to_datetime, concat
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, RANSACRegressor, ARDRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from scipy.signal import savgol_filter

dataset = read_csv('../data/data_smoothed.csv', delimiter=';')
dataset['date'] = to_datetime(dataset['date'])
dataset = dataset.drop([0, 1, 2])

dataset = dataset.drop(['date'], axis=1)

y_labels = ['p_v', 'q_v']

n_tests = dataset.shape[0]

max_abs_error = -1e10
min_abs_error = 1e10
tests_errors = DataFrame({
    'p_v': [],
    'q_v': []
})

has_random = True
overall_test_time = 0.0

for i in range(n_tests):
    t = i + 3
    test_line = dataset.loc[[t]]
    train_lines = dataset.drop([t])

    y_train = train_lines[y_labels]
    y_test = test_line[y_labels]
    x_train = train_lines.drop(y_labels, axis=1)
    x_test = test_line.drop(y_labels, axis=1)

    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.01)

    model = MultiOutputRegressor(SVR(kernel='linear', C=0.2, epsilon=0.05, gamma='scale'))
    t_start = time.time()
    model.fit(x_train, y_train)
    y_result = model.predict(x_test)
    t_end = time.time()

    overall_test_time += (t_end - t_start)
    abs_errors = 100 * abs((y_result - y_test.values) / y_test)
    #rmse r2
    test_errors = concat([tests_errors, abs_errors])

print(f"AFTER {n_tests} ITERATIONS")
print('total avg. error %:')
print(test_errors.sum() / n_tests)
print(f'avg. prediction time: {1000 * overall_test_time / n_tests} ms')
