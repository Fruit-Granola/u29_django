import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# 学習するモデル
class Trainer:
    def __init__(self):
        self.x_train = pd.read_csv("train_x.csv", low_memory=False)
        self.y_train = pd.read_csv("train_y.csv", low_memory=False)

    def Process(self):
        self.x_train = self.x_train.drop("お仕事No.", axis=1)

        for column in self.x_train.columns:
            if self.x_train[column].nunique() < 2:
                self.x_train = self.x_train.drop(column, axis=1)

        for column in self.x_train.columns:
            if  self.x_train[column].dtype == "object":
                self.x_train = self.x_train.drop(column, axis=1)

        self.x_train = self.x_train.fillna(0)

        self.y_train_array = np.array(self.y_train["応募数 合計"])
        self.X_train_array = np.array(self.x_train)

        self.rfr = RandomForestRegressor(random_state=0)
        self.rfr.fit(self.X_train_array, self.y_train_array)

        return self.x_train, self.rfr

# 学習されたモデルから予測を出す
class Predictor:
    def __init__(self, csv):
        self.x_data = pd.read_csv(csv, low_memory=False)
        self.work_num = self.x_data["お仕事No."]

    def FitToTrain(self, x_train):
        self.x_data.dropna(how="all", axis=1)
        for column in self.x_data.columns:
            if not column in x_train.columns:
                self.x_data = self.x_data.drop(column, axis=1)


    def FillNa(self):
        self.x_data = self.x_data.fillna(0)

    def DataToArray(self):
        self.X_test_array = np.array(self.x_data)

    def Prediction(self, model):
        try:
            self.y_pred = model.predict(self.X_test_array)
        except:
            print(self.x_data.info())
    def ToSubmitFormat(self):
        self.y_pred_submit = pd.DataFrame({
            "お仕事No.": self.work_num,
            "応募数 合計": self.y_pred
        })
        return self.y_pred_submit
