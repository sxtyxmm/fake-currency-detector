<!-- # 💵 Fake Currency Detection using Machine Learning

A web application built with **Flask**, **TensorFlow**, and **TailwindCSS** that allows users to upload currency images and get a prediction on whether the currency is **Real** or **Fake**, along with a confidence score.

---

## 🚀 Features

- 📷 Upload currency images (JPG, JPEG, PNG)
- ✅ Detect Real or Fake currency using a trained ML model
- 📊 View prediction logs in an admin dashboard
- 🔐 Secure admin login with hashed password
- 📁 Download logs as CSV
- 🧪 Fully tested with `pytest` and `Flask` test client
- 🎨 Responsive and clean UI using TailwindCSS

---

## 🧠 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, TailwindCSS
- **ML Framework:** TensorFlow / Keras
- **Database:** SQLite (via `sqlite3`)
- **Testing:** pytest, coverage
- **Deployment-ready:** GitHub Codespaces compatible

---

## 🏁 Getting Started

### 🔧 Prerequisites

- Python 3.10+
- pip
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

---

### 🛠 Installation

```bash
git clone https://github.com/yourusername/fake-currency-detector.git
cd fake-currency-detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### ▶️ Run the App

```bash
python app/routes.py
```

App will be available at `http://localhost:5000/`

---

## 🔐 Admin Login

| Username | Password   |
|----------|------------|
| `admin`  | `pass123` |

- View prediction history
- Download prediction logs as CSV

---

## 🧪 Run Tests

```bash
pytest
```

Or with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## 📁 Folder Structure

```
fake-currency-detector/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── database.py
│   ├── static/
│   └── templates/
├── model/
│   └── model.h5
├── tests/
│   └── test_app.py
├── requirements.txt
└── README.md
```

---

## 💡 Future Enhancements

- 🔄 Model retraining pipeline
- 📈 Confidence chart improvements
- 👨‍💻 Role-based access (multi-admin support)
- ☁️ Cloud deployment on Render/Vercel/Heroku

---

## 📸 Screenshots

| Upload Page | Admin Dashboard |
|-------------|-----------------|
| ![upload](screenshots/upload.png) | ![admin](screenshots/admin.png) |

---

## 📜 License

MIT License © 2025 [Satyam Singh Shishodiya] -->
# 💵 Fake Currency Detection using Machine Learning

A production-ready web application built with **Flask**, **TensorFlow**, and **TailwindCSS** that allows users to upload currency images and get a prediction on whether the currency is **Real** or **Fake**, along with a confidence score.

---

## 🚀 Features

- 📷 Upload currency images (JPG, JPEG, PNG)
- ✅ Detect Real or Fake currency using a trained ML model
- 📊 View prediction logs in an admin dashboard
- 🔐 Secure admin login with hashed password
- 📁 Download logs as CSV
- 🧹 Clear logs with one click
- 📈 View Real vs Fake prediction chart (Chart.js)
- 🧪 Fully tested with `pytest` and `Flask` test client
- 🌐 Production-ready structure with `.env` and `gunicorn` support
- 🎨 Responsive and clean UI using TailwindCSS

---

## 🧠 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, TailwindCSS, Chart.js
- **ML Framework:** TensorFlow / Keras
- **Database:** SQLite (via `sqlite3`)
- **Testing:** pytest, coverage
- **Deployment-ready:** Docker, GitHub Codespaces, Gunicorn

---

## 🏁 Getting Started

### 🔧 Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)

---

### 🛠 Installation

```bash
git clone https://github.com/yourusername/fake-currency-detector.git
cd fake-currency-detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### ▶️ Run the App (Dev)

```bash
python run.py
```

Or using Gunicorn for production:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app.routes:app
```

---

## 🔁 Model Training

Train your own model using a labeled dataset.

### 📁 Dataset Structure

```
dataset/
├── train/
│   ├── real/
│   └── fake/
└── test/
    ├── real/
    └── fake/
```

### 🧠 Architecture

- CNN (Conv2D + MaxPooling)
- Flatten → Dense → Dropout → Sigmoid

### 🏋️ Train the Model

```bash
python train_model.py
```

This will output the trained model at:

```
app/model/currency_cnn.h5
```

---

## 🔐 Admin Login

| Username | Password   |
|----------|------------|
| `admin`  | `pass123` |

- View logs
- Download as CSV
- Clear all logs with one click

---

## 🧪 Run Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## 📁 Folder Structure

```
fake-currency-detector/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── database.py
│   ├── model/
│   ├── static/
│   └── templates/
├── dataset/
├── tests/
├── train_model.py
├── run.py
├── requirements.txt
├── .env (optional)
└── README.md
```

---

## 💡 Future Enhancements

- 🔄 Retrain UI
- 🧠 Model metrics dashboard
- 🔑 Multi-admin roles
- ☁️ Deployment on Render/Vercel/Docker/Heroku

---

## 📸 Screenshots

| Upload | Admin Panel |
|--------|--------------|
| ![upload](screenshots/upload.png) | ![admin](screenshots/admin.png) |

---

## 📜 License

MIT License © 2025 [Satyam Singh Shishodiya]
