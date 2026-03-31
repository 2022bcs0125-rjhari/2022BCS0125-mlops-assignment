import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import numpy as np
import os
import json
from preprocess import preprocess

ROLL_NO = "2022BCS0125"
NAME = "R J Hari"

mlflow.set_experiment(f"{ROLL_NO}_experiment")


def train():
    df = pd.read_csv("data/train.csv")

    # Remove extreme outliers
    df = df[(df["trip_duration"] > 10) & (df["trip_duration"] < 20000)]

    X = preprocess(df)
    y = df["trip_duration"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run():
        model = RandomForestRegressor(n_estimators=100, max_depth=10)

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        # Log to MLflow
        mlflow.log_param("model", "RandomForest")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(model, "model")

        # Save model
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")

        # Save metrics.json
        metrics = {
            "rmse": float(rmse),
            "r2": float(r2),
            "name": NAME,
            "roll_no": ROLL_NO
        }

        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)


        print(f"RMSE: {rmse}, R2: {r2}")


if __name__ == "__main__":
    train()