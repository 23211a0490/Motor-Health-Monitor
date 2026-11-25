
import numpy as np
import pandas as pd
import joblib
 
from sklearn.ensemble import (
 
    RandomForestClassifier,
    RandomForestRegressor
 
)
 
from config import MODEL_FILE
 
 
# ==========================================
# RANDOM SEED
# ==========================================
 
np.random.seed(42)
 
 
# ==========================================
# MOTOR CONDITIONS
# ==========================================
 
SCENARIOS = {
 
    "Normal": {
 
        "vibration": 0.12,
        "temperature": 30,
        "current": 0.80,
        "rpm": 1500,
        "health": 95
 
    },
 
 
    "Imbalance": {
 
        "vibration": 0.52,
        "temperature": 34,
        "current": 0.90,
        "rpm": 1480,
        "health": 72
 
    },
 
 
    "Overload": {
 
        "vibration": 0.35,
        "temperature": 45,
        "current": 1.35,
        "rpm": 1380,
        "health": 62
 
    },
 
 
    "Degraded": {
 
        "vibration": 0.65,
        "temperature": 48,
        "current": 1.25,
        "rpm": 1360,
        "health": 45
 
    }
 
}
 
 
# ==========================================
# CREATE DATASET
# ==========================================
 
rows = []
 
 
for condition, values in SCENARIOS.items():
 
 
    for _ in range(800):
 
 
        voltage = np.random.normal(
 
            12.0,
 
            0.3
 
        )
 
 
        current = max(
 
            0.1,
 
            np.random.normal(
 
                values["current"],
 
                0.08
 
            )
 
        )
 
 
        temperature = np.random.normal(
 
            values["temperature"],
 
            2
 
        )
 
 
        vibration = max(
 
            0.01,
 
            np.random.normal(
 
                values["vibration"],
 
                0.05
 
            )
 
        )
 
 
        rpm = max(
 
            100,
 
            np.random.normal(
 
                values["rpm"],
 
                30
 
            )
 
        )
 
 
        power = voltage * current
 
 
        vibration_peak = vibration * 1.7
 
 
        operating_hours = np.random.uniform(
 
            100,
 
            1000
 
        )
 
 
        health = np.clip(
 
            np.random.normal(
 
                values["health"],
 
                5
 
            ),
 
            0,
 
            100
 
        )
 
 
        rows.append({
 
            "voltage": voltage,
 
            "current": current,
 
            "power_w": power,
 
            "temperature": temperature,
 
            "rpm": rpm,
 
            "vibration_rms": vibration,
 
            "vibration_peak": vibration_peak,
 
            "operating_hours": operating_hours,
 
            "condition": condition,
 
            "health_score": health
 
        })
 
 
# ==========================================
# DATAFRAME
# ==========================================
 
df = pd.DataFrame(rows)
 
 
print()
 
print("DATASET CREATED")
 
print("Total Samples:", len(df))
 
print()
 
print(
 
    df["condition"].value_counts()
 
)
 
 
# ==========================================
# FEATURES
# ==========================================
 
FEATURES = [
 
    "voltage",
 
    "current",
 
    "power_w",
 
    "temperature",
 
    "rpm",
 
    "vibration_rms",
 
    "vibration_peak",
 
    "operating_hours"
 
]
 
 
X = df[FEATURES]
 
 
# ==========================================
# CLASSIFICATION MODEL
# ==========================================
 
classifier = RandomForestClassifier(
 
    n_estimators=200,
 
    random_state=42
 
)
 
 
classifier.fit(
 
    X,
 
    df["condition"]
 
)
 
 
# ==========================================
# REGRESSION MODEL
# ==========================================
 
regressor = RandomForestRegressor(
 
    n_estimators=200,
 
    random_state=42
 
)
 
 
regressor.fit(
 
    X,
 
    df["health_score"]
 
)
 
 
# ==========================================
# SAVE MODEL
# ==========================================
 
model = {
 
    "features": FEATURES,
 
    "classifier": classifier,
 
    "regressor": regressor
 
}
 
 
joblib.dump(
 
    model,
 
    MODEL_FILE
 
)
 
 
print()
 
print("================================")
 
print("AI MODEL TRAINED SUCCESSFULLY")
 
print("================================")
 
print()
 
print("Model File:", MODEL_FILE)