from fastapi import FastAPI
import joblib
import pandas as pd
from src.preprocess import preprocess

ROLL_NO = "2022BCS0125"
NAME = "R J Hari"

app = FastAPI()

model = joblib.load("models/model.pkl")


@app.get("/")
def health():
    return {
        "Name": NAME,
        "Roll No": ROLL_NO
    }


@app.post("/predict")
def predict(data: dict):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data])

        expected_features = model.n_features_in_

        if expected_features == 2:
            X = preprocess(df, use_selected_features=True)
        else:
            X = preprocess(df, use_selected_features=False)

        prediction = model.predict(X)[0]

        return {
            "prediction": float(prediction),
            "Name": NAME,
            "Roll No": ROLL_NO
        }

    except Exception as e:
        return {"error": str(e)}