from flask import Flask, request, render_template
import os
import time
import threading
import numpy as np
from app.database import log_prediction
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Store only the hashed password
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("pass123")  # Replace "pass123" if needed

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "super-secret-key"  # for session cookies

# Load trained model
model = load_model('app/model/currency_cnn.h5')

# Allowed extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# Validate file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Prepare image for prediction
def prepare_image(image_path):
    img = load_img(image_path, target_size=(128, 128))
    img_array = img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# Auto-delete image after response
def delayed_delete(path):
    try:
        time.sleep(5)
        os.remove(path)
        print(f"[Auto-Delete] Removed: {path}")
    except Exception as e:
        print(f"[Auto-Delete Failed] {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("currency")
        if not file:
            return "No file uploaded", 400

        if not allowed_file(file.filename):
            return "Only JPG, JPEG, PNG files are allowed", 400

        filename = secure_filename(file.filename)
        file_path = os.path.join("app/static", filename)
        file.save(file_path)

        # Make prediction
        img = prepare_image(file_path)
        prediction = model.predict(img)[0][0]

        # Adjust confidence for displayed class
        if prediction > 0.5:
            final_confidence = round(prediction * 100, 2)
            result = f"Real Currency (Confidence: {final_confidence}%)"
        else:
            final_confidence = round((1 - prediction) * 100, 2)
            result = f"Fake Currency (Confidence: {final_confidence}%)"
        
        # Log prediction to SQLite
        label = "Real" if prediction > 0.5 else "Fake"
        log_prediction(filename, label, final_confidence)

        # Schedule image deletion
        threading.Thread(target=delayed_delete, args=(file_path,)).start()

        # Show result
        return render_template("result.html", result=result, image=filename, confidence=final_confidence)

    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    import sqlite3
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
            flash("Invalid credentials", "error")  # flash the error
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
    import csv
    from flask import Response
    import io
    import sqlite3

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow(["Filename", "Label", "Confidence (%)", "Timestamp"])

    # Fetch logs
    with sqlite3.connect("predictions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filename, label, confidence, timestamp FROM predictions ORDER BY id DESC")
        logs = cursor.fetchall()

    # Write data
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
    import sqlite3
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

    import sqlite3
    with sqlite3.connect("predictions.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()
    return redirect(url_for("admin"))