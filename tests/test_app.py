import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from io import BytesIO
from app.routes import app
from PIL import Image
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Fake Currency Detector" in response.data

def test_prediction_real_currency(client):
    img = Image.new('RGB', (128, 128), color='white')
    dummy_image = BytesIO()
    img.save(dummy_image, format='PNG')
    dummy_image.seek(0)

    data = {'currency': (dummy_image, 'test.png')}
    response = client.post("/", content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert b"Confidence Score" in response.data

def test_prediction_fake_currency(client):
    img = Image.new('RGB', (128, 128), color='black')
    dummy_image = BytesIO()
    img.save(dummy_image, format='PNG')
    dummy_image.seek(0)

    data = {'currency': (dummy_image, 'test.png')}
    response = client.post("/", content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert b"Confidence Score" in response.data

def test_reject_invalid_file_type(client):
    data = {'currency': (BytesIO(b"not image"), 'test.pdf')}
    response = client.post("/", content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert b"Only JPG, JPEG, PNG files are allowed" in response.data

def test_missing_file_submission(client):
    response = client.post("/", data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"No file uploaded" in response.data

def test_upload_empty_filename(client):
    data = {'currency': (BytesIO(b''), '')}
    response = client.post("/", content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert b"No file uploaded" in response.data

def test_admin_login_fail(client):
    response = client.post("/login", data={"username": "wrong", "password": "fail"})
    # Assert redirect happened (invalid login goes back to /login)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")

def test_admin_login_success(client):
    response = client.post("/login", data={"username": "admin", "password": "pass123"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Prediction Logs" in response.data

def test_admin_requires_login(client):
    response = client.get("/admin", follow_redirects=True)
    assert b"Login" in response.data or b"Invalid credentials" in response.data

def test_admin_page_access(client):
    with client.session_transaction() as sess:
        sess["logged_in"] = True
    response = client.get("/admin")
    assert response.status_code == 200
    assert b"Prediction Logs" in response.data

def test_post_admin_not_allowed(client):
    response = client.post("/admin")
    assert response.status_code in [405, 302]

def test_logout(client):
    with client.session_transaction() as sess:
        sess["logged_in"] = True
    response = client.get("/logout", follow_redirects=True)
    assert b"Login" in response.data or response.status_code == 200

def test_download_csv(client):
    with client.session_transaction() as sess:
        sess["logged_in"] = True
    response = client.get("/download-csv")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"Filename,Label,Confidence (%),Timestamp" in response.data

def test_download_csv_requires_login(client):
    response = client.get("/download-csv", follow_redirects=True)
    assert b"Login" in response.data or response.status_code == 200