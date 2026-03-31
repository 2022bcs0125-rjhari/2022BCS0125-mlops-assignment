import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius (km)
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def preprocess(df):
    df = df.copy()

    # Convert datetime
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])

    # Feature engineering
    df["pickup_hour"] = df["pickup_datetime"].dt.hour

    df["distance"] = haversine(
        df["pickup_latitude"],
        df["pickup_longitude"],
        df["dropoff_latitude"],
        df["dropoff_longitude"]
    )

    # Select features
    features = [
        "passenger_count",
        "pickup_hour",
        "distance"
    ]

    X = df[features]

    return X