import sqlite3
from datetime import datetime

def init_db():
    with sqlite3.connect("predictions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                label TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()

def log_prediction(filename, label, confidence):
    # Ensure confidence is a float
    try:
        confidence = float(confidence)
    except:
        confidence = 0.0

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect("predictions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (filename, label, confidence, timestamp)
            VALUES (?, ?, ?, ?)
        """, (filename, label, confidence, timestamp))
        conn.commit()