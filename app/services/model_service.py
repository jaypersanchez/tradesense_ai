
from sklearn.linear_model import LinearRegression
import pandas as pd

class PredictionModel:
    def train_and_predict(self, df):
        df = df.copy()
        df["time"] = df["timestamp"].astype("int64") // 10**9
        df["price"] = df["price"].astype(float)

        X = df["time"].values.reshape(-1, 1)
        y = df["price"].values

        model = LinearRegression()
        model.fit(X, y)
        df["predicted"] = model.predict(X)
        return df
