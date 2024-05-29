import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from pandas import read_csv, to_datetime
from scipy.signal import savgol_filter
from matplotlib.cbook import boxplot_stats

if __name__ == '__main__':
    smoothed_data = read_csv('./data_smoothed_restored.csv', delimiter=';')
    restored_data = read_csv('./data_restored.csv', delimiter=';')

    smoothed_data['date'] = to_datetime(smoothed_data['date'])
    restored_data['date'] = to_datetime(restored_data['date'])

    print(smoothed_data.corr())