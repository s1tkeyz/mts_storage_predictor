from numpy import nan
from pandas import read_csv, DataFrame
from sklearn.impute import IterativeImputer

if __name__ == '__main__':
    dataset = read_csv('data.csv')
    dataset = dataset.drop(['date'], axis=1)

    dataset = dataset.replace(-1, nan)

    values = dataset.values

    imputer = IterativeImputer(random_state=0)

    transformed_values = imputer.fit_transform(values)

    dataset = DataFrame(transformed_values, columns=dataset.columns)
    dataset.to_csv("data_restored_i.csv")
