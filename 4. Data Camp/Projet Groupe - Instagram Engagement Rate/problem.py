import os

import numpy as np
import pandas as pd
import rampwf as rw
from rampwf.score_types.base import BaseScoreType
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_squared_error


problem_title = 'Prediction of the engagement rate'
_target_column_name = 'ER'
# A type (class) which will be used to create wrapper objects for y_pred
Predictions = rw.prediction_types.make_regression()
# An object implementing the workflow
workflow = rw.workflows.Estimator()


class RMSE(BaseScoreType):
    is_lower_the_better = True
    minimum = 0.0
    maximum = float('inf')

    def __init__(self, name='rmse', precision=5):
        self.name = name
        self.precision = precision

    def __call__(self, y_test, y_pred):
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        return rmse 


score_types = [
    RMSE(name='RMSE', precision=5),
]


def get_cv(X, y):
    cv = ShuffleSplit(n_splits=8, test_size=0.20, random_state=42)
    return cv.split(X, y)


def _read_data(path, f_name):
    data = pd.read_csv(os.path.join(path, 'data', f_name))
    y_array = data[_target_column_name].values
    X_df = data.drop(_target_column_name, axis=1)
    return X_df, y_array


def get_train_data(path='.'):
    f_name = 'train.csv'
    return _read_data(path, f_name)


def get_test_data(path='.'):
    f_name = 'test.csv'
    return _read_data(path, f_name)