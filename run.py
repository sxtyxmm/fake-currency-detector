from app.routes import app
from app.database import init_db

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)