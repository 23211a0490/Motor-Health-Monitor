
import json
import joblib
 
import pandas as pd
 
 
from config import (
 
    MODEL_FILE,
 
    LATEST_DATA_FILE
 
)
 
 
# ==========================================
# LOAD AI MODEL
# ==========================================
 
model = joblib.load(
 
    MODEL_FILE
 
)
 
 
FEATURES = model[
 
    "features"
 
]
 
 
classifier = model[
 
    "classifier"
 
]
 
 
regressor = model[
 
    "regressor"
 
]
 
 
# ==========================================
# AI PREDICTION
# ==========================================
 
def predict_motor_health(data):
 
 
    # --------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------
 
    X = pd.DataFrame(
 
        [[
 
            data.get(
 
                feature,
 
                0
 
            )
 
            for feature in FEATURES
 
        ]],
 
        columns=FEATURES
 
    )
 
 
    # --------------------------------------
    # CLASSIFICATION
    # --------------------------------------
 
    condition = classifier.predict(
 
        X
 
    )[0]
 
 
    probabilities = (
 
        classifier.predict_proba(
 
            X
 
        )[0]
 
    )
 
 
    confidence = float(
 
        max(
 
            probabilities
 
        ) * 100
 
    )
 
 
    # --------------------------------------
    # HEALTH SCORE
    # --------------------------------------
 
    health_score = float(
 
        regressor.predict(
 
            X
 
        )[0]
 
    )
 
 
    health_score = max(
 
        0,
 
        min(
 
            100,
 
            health_score
 
        )
 
    )
 
 
    # --------------------------------------
    # RESULT
    # --------------------------------------
 
    result = {
 
        "timestamp":
 
            data["timestamp"],
 
 
        "motor_id":
 
            data["motor_id"],
 
 
        "condition":
 
            condition,
 
 
        "health_score":
 
            round(
 
                health_score,
 
                2
 
            ),
 
 
        "confidence":
 
            round(
 
                confidence,
 
                2
 
            )
 
    }
 
 
    return result
 
 
# ==========================================
# SAVE LATEST DATA
# ==========================================
 
def save_latest_data(
 
    data,
 
    prediction
 
):
 
 
    output = {
 
        "sensor_data":
 
            data,
 
 
        "ai_prediction":
 
            prediction
 
    }
 
 
    with open(
 
        LATEST_DATA_FILE,
 
        "w"
 
    ) as file:
 
 
        json.dump(
 
            output,
 
            file,
 
            indent=4
 
        )