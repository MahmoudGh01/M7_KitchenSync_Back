# app.py

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

from app.Models.UserModel import db, User
from app.Routes.AuthRoutes import auth_ns

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "mysql+pymysql://root:@localhost:3306/KitchenSync"

app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900      # 15 min
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 604800  # 7 days

db.init_app(app)
jwt = JWTManager(app)
api = Api(app, doc="/docs")
api.add_namespace(auth_ns)

with app.app_context():
    try:
        db.engine.connect()
        print("✅ Connected successfully")
    except Exception as e:
        print("❌ Connection failed:", e)
    db.create_all()
