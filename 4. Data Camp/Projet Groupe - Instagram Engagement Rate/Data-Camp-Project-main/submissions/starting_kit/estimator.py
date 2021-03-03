import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor


def processing_data(X):
    
    X['media_type'] = X['media_type'].replace({'Photo':0,'Video':1})
    X["Day_week"] = LabelEncoder().fit_transform(X['Day_week'])
    X['sentiment'] = X['sentiment'].replace({'neutral':0,'positive':1,'negative':-1})
 
    return np.c_[X['sentiment'].values,X['media_type'].values,
                X['Day_week'].values]
                  

transformer_var = FunctionTransformer(
    lambda df: processing_data(df)
)
                 
cols = ['num_posts', 'num_followings','year', 'month', 'day', 'hour',
        'num_words','polarity', 'num_hashtags','num_ref', 'dominant_topic',
        'perc_contribution']

                 

transformer = make_column_transformer(
    (transformer_var, ['media_type', 'sentiment','Day_week']),
    (OneHotEncoder(), ['pr_activity']),
    ('passthrough', cols),
)

pipe = make_pipeline(
    transformer,
    StandardScaler(),
    RandomForestRegressor()
)
    
def get_estimator():
    return pipe