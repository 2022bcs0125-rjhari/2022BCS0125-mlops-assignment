from fastapi import FastAPI
import joblib
import numpy as np

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
        features = np.array([[
            data["passenger_count"],
            data["pickup_hour"],
            data["distance"]
        ]])

        prediction = model.predict(features).tolist()

        return {
            "prediction": prediction,
            "Name": NAME,
            "Roll No": ROLL_NO
        }

    except Exception as e:
        return {"error": str(e)}