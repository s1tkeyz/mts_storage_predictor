from matplotlib import pyplot as plt, use
use('tkagg')

from numpy import nan, mean
from pandas import read_csv, DataFrame, to_datetime
""" from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.impute import KNNImputer """
from prophet import Prophet
from scipy.signal import savgol_filter

Y = 'p_v'
FORECAST_L = 3


sdataset = read_csv('DATA_RESTORED.csv', delimiter=';')
sdataset['date'] = to_datetime(sdataset['date'])
sdataset = sdataset.drop([0, 1, 2, 39, 40, 41, 42, 43, 44, 45])

sdataset['p_v'] = savgol_filter(sdataset['p_v'], 10, 3)
sdataset['q_v'] = savgol_filter(sdataset['q_v'], 10, 3)

sdataset = sdataset.reindex()
print(sdataset)
print(sdataset.shape)
DATA_LENGTH = sdataset.shape[0] - 1
train_set = sdataset.drop(range(DATA_LENGTH, DATA_LENGTH - FORECAST_L, -1))
# train_set['rolling_x'] = train_set[Y].rolling(window=FORECAST_L * 2).mean()
m = Prophet()

prophet_df = DataFrame(train_set[['date', Y]].values, columns=['ds', 'y'])
#prophet_df.loc[(prophet_df['ds'] > '2021-02-01') & (prophet_df['ds'] < '2021-11-01'), 'y'] = None

m.fit(prophet_df)
future = m.make_future_dataframe(periods=FORECAST_L, freq='ME')
forecast = m.predict(future)

cmp_df = forecast[['yhat']].join(prophet_df['y'])
cmp_df['e'] = cmp_df['y'] - cmp_df['yhat']
cmp_df['p'] = 100 * cmp_df['e'] / cmp_df['y']

print('MAPE = {:.2f}%'.format(mean(abs(cmp_df[-FORECAST_L:]["p"]))))
print('MAE = {:.3f} m^3'.format(mean(abs(cmp_df[-FORECAST_L:]["e"]))))

m.plot(forecast)
plt.plot(sdataset['date'], sdataset[Y], 'r')
plt.grid(True)
plt.show()