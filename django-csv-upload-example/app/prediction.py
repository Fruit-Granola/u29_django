import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class Trainer:
    def __init__(self):
        x_train = pd.read_csv("train_x.csv")
        y_train = pd.read_csv("train_y.csv")
        self.x_train = x_train
        self.y_train = y_train


    def Process():
        x_train = x_train.drop("お仕事No.", axis=1)
        for column in x_train.columns:
            if x_train[column].nunique() < 2:
                x_train = x_train.drop(column, axis=1)
        x_train = x_train.fillna(0)
        for column in x_train.columns:
            if  x_train[column].dtype == "object":
                x_train = x_train.drop(column, axis=1)

        y_train_array = np.array(y_train["応募数 合計"])
        X_train_array = np.array(x_train)

        self.rfr = rfr
        rfr = RandomForestRegressor(random_state=0)
        rfr.fit(self.X_train_array, self.y_train_array)
        return x_train, rfr

class Predictor:
    def __init__(self, csv):
        self.x_data = pd.read_csv(csv)
        self.work_num = self.x_data["お仕事No."]

    def FitToTrain(self, x_train):
        for column in self.x_data.columns:
            if not column in x_train.columns:
                self.x_data = self.x_data.drop(column, axis=1)

    def DataToArray(self):
        self.X_test_array = np.array(self.x_data)

    def Prediction(self, model):
        self.y_pred = model.predict(self.X_test_array)

    def ToSubmitFormat(self):
        self.y_pred_submit = pd.DataFrame({
            "お仕事No.": self.work_num,
            "応募数 合計": self.y_pred
        })

    def fill_na(self):
        self.x_data = self.x_data.fillna(0)

    def drop_object(self):
        for column in self.x_data.columns:
            if  self.x_data[column].dtype == "object":
                self.x_data = self.x_data.drop(column, axis=1)
