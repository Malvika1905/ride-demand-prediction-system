import pandas as pd

def create_features(df):
    df = pd.get_dummies(df, columns=['h3_cell'], drop_first=True)

    features = ['hour', 'day_of_week', 'weather_flag'] + \
               [col for col in df.columns if col.startswith('h3_cell_')]

    return df, features