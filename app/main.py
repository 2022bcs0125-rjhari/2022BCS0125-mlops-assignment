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

        # Apply SAME preprocessing
        X = preprocess(df)

        prediction = model.predict(X)[0]

        return {
            "prediction": float(prediction),
            "Name": NAME,
            "Roll No": ROLL_NO
        }

    except Exception as e:
        return {"error": str(e)}