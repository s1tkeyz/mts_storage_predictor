from numpy import nan
import pandas as pd
from pandas import read_csv, DataFrame
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

if __name__ == '__main__':
    df = pd.read_excel('send fact.xlsx')
    data = pd.DataFrame(columns=['year', 'month', 'data'])
    data['year'] = df['Unnamed: 0']
    data['month'] = df['Unnamed: 1']
    count = 0
    for index, row in data.iterrows():
        data.at[index, 'data'] = count
        count += 1
    df = df.drop(columns=['Unnamed: 0', 'Unnamed: 1'])
    df = df.replace(0, nan)

    values = df.values
    imputer = IterativeImputer(random_state=0)
    transformed_values = imputer.fit_transform(values)
    df = DataFrame(transformed_values, columns=df.columns)
    df['year'] = data['year']
    df['month'] = data['month']
    df['data'] = data['data']
    for index, row in df.iterrows():
        for name in df.columns:
            if df.at[index, name] < 0:
                df.at[index, name] = 0
    print(df)
    df.to_csv("send fact restored.csv")