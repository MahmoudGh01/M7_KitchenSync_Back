from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "mysql+pymysql://root:@localhost:3306/KitchenSync"

db = SQLAlchemy(app)

with app.app_context():
    try:
        db.engine.connect()
        print("✅ Connected successfully")
    except Exception as e:
        print("❌ Connection failed:", e)
