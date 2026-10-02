from pathlib import Path

import pandas as pd
from catboost import CatBoostClassifier

from preprocessing import add_features

MODEL_PATH = Path(__file__).parent / "models" / "catboost_fraud.cbm"
THRESHOLD = 0.95

NUM_FEATURES = [
    "amount", "amount_log", "population_city", "population_log", "distance_km",
    "lat", "lon", "merchant_lat", "merchant_lon",
    "hour", "dayofweek", "day", "month", "is_night",
]
CAT_FEATURES = [
    "merch", "cat_id", "gender", "us_state", "jobs",
    "name_1", "name_2", "one_city", "street", "post_code",
]
FEATURES = NUM_FEATURES + CAT_FEATURES

model = CatBoostClassifier()
model.load_model(str(MODEL_PATH))


def build_features(data):
    df = add_features(pd.DataFrame(data))
    X = df[FEATURES].copy()
    X[CAT_FEATURES] = X[CAT_FEATURES].astype(str)
    return X


def predict(data, threshold=THRESHOLD):
    X = build_features(data)
    score = model.predict_proba(X)[:, 1]
    return pd.DataFrame({
        "score": score,
        "fraud_flag": (score >= threshold).astype(int),
    })
