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

# IMPORTANT: Force MLflow to use local storage
mlflow.set_tracking_uri("file:./mlruns")

ROLL_NO = "2022BCS0125"
NAME = "R J Hari"

mlflow.set_experiment(f"{ROLL_NO}_experiment")

# CONFIG (EDIT PER COMMIT) 
DATA_VERSION = "v2"
MODEL_TYPE = "rf"
USE_SELECTED_FEATURES = True

PARAMS = {
    "n_estimators": 200,
    "max_depth": 15
}
def train():

    # Dataset mapping
    file_map = {
        "v1": "data/train_small.csv",
        "v2": "data/train.csv"
    }

    df = pd.read_csv(file_map[DATA_VERSION])

    # Outlier removal
    df = df[(df["trip_duration"] > 10) & (df["trip_duration"] < 20000)]

    X = preprocess(df, USE_SELECTED_FEATURES)
    y = df["trip_duration"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ✅ IMPORTANT: Proper run naming
    run_name = f"{MODEL_TYPE}_{DATA_VERSION}_{'selected' if USE_SELECTED_FEATURES else 'all'}"

    with mlflow.start_run(run_name=run_name):

        # ================= MODEL =================
        if MODEL_TYPE == "rf":
            model = RandomForestRegressor(
                n_estimators=PARAMS.get("n_estimators", 100),
                max_depth=PARAMS.get("max_depth", 10),
                random_state=42
            )

        elif MODEL_TYPE == "ridge":
            from sklearn.linear_model import Ridge
            model = Ridge(alpha=PARAMS.get("alpha", 1.0))

        # ================= TRAIN =================
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        # ================= LOG PARAMS =================
        mlflow.log_param("data_version", DATA_VERSION)
        mlflow.log_param("model_type", MODEL_TYPE)
        mlflow.log_param("features", "selected" if USE_SELECTED_FEATURES else "all")

        for k, v in PARAMS.items():
            mlflow.log_param(k, v)

        # ================= LOG METRICS =================
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        # ================= SAVE FILES =================
        os.makedirs("models", exist_ok=True)

        model_path = "models/model.pkl"
        joblib.dump(model, model_path)

        metrics = {
            "rmse": float(rmse),
            "r2": float(r2),
            "name": NAME,
            "roll_no": ROLL_NO
        }

        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

        # ================= LOG ARTIFACTS =================
        mlflow.sklearn.log_model(model, "model")
        mlflow.log_artifact("metrics.json")
        mlflow.log_artifact(model_path)

        print(f"[{MODEL_TYPE} | {DATA_VERSION}] RMSE: {rmse}, R2: {r2}")


if __name__ == "__main__":
    train()