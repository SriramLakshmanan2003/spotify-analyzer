import pandas as pd

def get_min_max_avg(df):
    return {
        'min_duration': df['duration_min'].min(),
        'max_duration': df['duration_min'].max(),
        'avg_duration': df['duration_min'].mean()
    }

def detect_duplicates(df):
    dup = df[df.duplicated(['track_name', 'artist_name', 'duration_min'], keep=False)]
    return dup.drop_duplicates(['track_name', 'artist_name', 'duration_min'])

def detect_outliers(df):
    q1 = df['duration_min'].quantile(0.25)
    q2 = df['duration_min'].quantile(0.75)
    iqr = q2 - q1
    lower = q1 - 1.5 * iqr
    upper = q2 + 1.5 * iqr
    return df[(df['duration_min'] < lower) | (df['duration_min'] > upper)]

