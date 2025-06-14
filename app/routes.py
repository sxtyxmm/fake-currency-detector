from flask import Flask, request, render_template, redirect, url_for, session, flash, Response
import os
import uuid
import numpy as np
import io
import csv
import sqlite3
from app.database import log_prediction
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# Config
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("pass123")

app = Flask(__name__)
app.secret_key = "super-secret-key"

# Load model
model = load_model("app/model/currency_cnn.keras")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_image(path):
    img = load_img(path, target_size=(128, 128))
    arr = img_to_array(img) / 255.0
    return np.expand_dims(arr, axis=0)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("currency")
        if not file:
            return "No file uploaded", 400
        if not allowed_file(file.filename):
            return "Only JPG, JPEG, PNG files are allowed", 400

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join("app/static", filename)
        file.save(filepath)

        img = prepare_image(filepath)
        pred = model.predict(img)[0][0]
        confidence = round((pred if pred > 0.5 else 1 - pred) * 100, 2)
        label = "Real" if pred > 0.5 else "Fake"
        result = f"{label} Currency (Confidence: {confidence}%)"

        log_prediction(filename, label, confidence)
        return render_template("result.html", result=result, image=filename, confidence=confidence)

    return render_template("index.html")

@app.route("/admin", methods=["GET"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    with sqlite3.connect("predictions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filename, label, confidence, timestamp FROM predictions ORDER BY id DESC")
        logs = cursor.fetchall()
    return render_template("admin.html", logs=logs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username != ADMIN_USERNAME or not check_password_hash(ADMIN_PASSWORD_HASH, password):
            flash("Invalid credentials", "error")
            return redirect(url_for("login"))
        session["logged_in"] = True
        return redirect(url_for("admin"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/download-csv")
def download_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Filename", "Label", "Confidence (%)", "Timestamp"])

    with sqlite3.connect("predictions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filename, label, confidence, timestamp FROM predictions ORDER BY id DESC")
        logs = cursor.fetchall()
        for row in logs:
            writer.writerow(row)

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=prediction_logs.csv"}
    )

@app.route("/chart-data")
def chart_data():
    with sqlite3.connect("predictions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT label, COUNT(*) FROM predictions GROUP BY label")
        results = cursor.fetchall()

    data = {"Real": 0, "Fake": 0}
    for label, count in results:
        data[label] = count

    return data

@app.route("/clear-logs", methods=["POST"])
def clear_logs():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    # Get list of filenames before clearing DB
    with sqlite3.connect("predictions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM predictions")
        files = cursor.fetchall()

        # Clear the DB
        cursor.execute("DELETE FROM predictions")
        conn.commit()

    # Delete images from static folder
    for (filename,) in files:
        path = os.path.join("app/static", filename)
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"[Deleted] {path}")
            except Exception as e:
                print(f"[Error deleting] {path}: {e}")

    return redirect(url_for("admin"))