
import sqlite3
 
from config import DATABASE_NAME
 
 
# ==========================================
# CREATE DATABASE
# ==========================================
 
def get_connection():
 
    connection = sqlite3.connect(
 
        DATABASE_NAME,
 
        check_same_thread=False
 
    )
 
    connection.row_factory = sqlite3.Row
 
    return connection
 
 
# ==========================================
# INITIALIZE DATABASE
# ==========================================
 
def initialize_database():
 
    connection = get_connection()
 
    cursor = connection.cursor()
 
 
    # --------------------------------------
    # SENSOR DATA TABLE
    # --------------------------------------
 
    cursor.execute("""
 
    CREATE TABLE IF NOT EXISTS motor_data(
 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        timestamp TEXT,
 
        motor_id TEXT,
 
        voltage REAL,
 
        current REAL,
 
        power_w REAL,
 
        temperature REAL,
 
        rpm REAL,
 
        vibration_rms REAL,
 
        vibration_peak REAL,
 
        operating_hours REAL
 
    )
 
    """)
 
 
    # --------------------------------------
    # AI PREDICTION TABLE
    # --------------------------------------
 
    cursor.execute("""
 
    CREATE TABLE IF NOT EXISTS ai_predictions(
 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        timestamp TEXT,
 
        motor_id TEXT,
 
        condition TEXT,
 
        health_score REAL,
 
        confidence REAL
 
    )
 
    """)
 
 
    # --------------------------------------
    # ALERT TABLE
    # --------------------------------------
 
    cursor.execute("""
 
    CREATE TABLE IF NOT EXISTS alerts(
 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        timestamp TEXT,
 
        motor_id TEXT,
 
        alert_type TEXT,
 
        severity TEXT,
 
        message TEXT
 
    )
 
    """)
 
 
    connection.commit()
 
    connection.close()
 
 
# ==========================================
# STORE MOTOR DATA
# ==========================================
 
def insert_motor_data(data):
 
    connection = get_connection()
 
    cursor = connection.cursor()
 
 
    cursor.execute("""
 
    INSERT INTO motor_data(
 
        timestamp,
        motor_id,
        voltage,
        current,
        power_w,
        temperature,
        rpm,
        vibration_rms,
        vibration_peak,
        operating_hours
 
    )
 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
 
    """,
 
    (
 
        data["timestamp"],
        data["motor_id"],
        data["voltage"],
        data["current"],
        data["power_w"],
        data["temperature"],
        data["rpm"],
        data["vibration_rms"],
        data["vibration_peak"],
        data["operating_hours"]
 
    ))
 
 
    connection.commit()
 
    connection.close()
 
 
# ==========================================
# STORE AI PREDICTION
# ==========================================
 
def insert_prediction(result):
 
    connection = get_connection()
 
    cursor = connection.cursor()
 
 
    cursor.execute("""
 
    INSERT INTO ai_predictions(
 
        timestamp,
        motor_id,
        condition,
        health_score,
        confidence
 
    )
 
    VALUES (?, ?, ?, ?, ?)
 
    """,
 
    (
 
        result["timestamp"],
        result["motor_id"],
        result["condition"],
        result["health_score"],
        result["confidence"]
 
    ))
 
 
    connection.commit()
 
    connection.close()
 
 
# ==========================================
# STORE ALERT
# ==========================================
 
def insert_alert(
 
    timestamp,
    motor_id,
    alert_type,
    severity,
    message
 
):
 
    connection = get_connection()
 
    cursor = connection.cursor()
 
 
    cursor.execute("""
 
    INSERT INTO alerts(
 
        timestamp,
        motor_id,
        alert_type,
        severity,
        message
 
    )
 
    VALUES (?, ?, ?, ?, ?)
 
    """,
 
    (
 
        timestamp,
        motor_id,
        alert_type,
        severity,
        message
 
    ))
 
 
    connection.commit()
 
    connection.close()
 
 
# ==========================================
# GET HISTORY
# ==========================================
 
def get_history(limit=100):
 
    connection = get_connection()
 
 
    rows = connection.execute("""
 
        SELECT *
 
        FROM motor_data
 
        ORDER BY id DESC
 
        LIMIT ?
 
    """,
 
    (limit,)
 
    ).fetchall()
 
 
    connection.close()
 
 
    return [
 
        dict(row)
 
        for row in reversed(rows)
 
    ]
 
 
# ==========================================
# GET ALERTS
# ==========================================
 
def get_alerts(limit=20):
 
    connection = get_connection()
 
 
    rows = connection.execute("""
 
        SELECT *
 
        FROM alerts
 
        ORDER BY id DESC
 
        LIMIT ?
 
    """,
 
    (limit,)
 
    ).fetchall()
 
 
    connection.close()
 
 
    return [
 
        dict(row)
 
        for row in rows
 
    ]
 
 
# ==========================================
# GET LATEST AI RESULT
# ==========================================
 
def get_latest_prediction():
 
    connection = get_connection()
 
 
    row = connection.execute("""
 
        SELECT *
 
        FROM ai_predictions
 
        ORDER BY id DESC
 
        LIMIT 1
 
    """).fetchone()
 
 
    connection.close()
 
 
    if row:
 
        return dict(row)
 
 
    return {}