import numpy as np
import pandas as pd


def distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return R * 2 * np.arcsin(np.sqrt(a))


def add_features(data):
    data = data.copy()
    t = pd.to_datetime(data["transaction_time"])
    data["hour"] = t.dt.hour
    data["dayofweek"] = t.dt.dayofweek
    data["day"] = t.dt.day
    data["month"] = t.dt.month
    data["is_night"] = ((t.dt.hour < 3) | (t.dt.hour >= 22)).astype(int)

    data["amount_log"] = np.log1p(data["amount"])
    data["population_log"] = np.log1p(data["population_city"])
    data["distance_km"] = distance(data["lat"], data["lon"], data["merchant_lat"], data["merchant_lon"])
    return data