# app.py

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

from app.extensions import db
from app.Models.UserModel import User
from app.Models.kitchen import Kitchen
from app.Models.item import Item
from app.Models.restock_log import RestockLog
from app.Models.consumption_log import ConsumptionLog
from app.Routes.AuthRoutes import auth_ns
from app.Routes.KitchenRoutes import kitchen_ns
from app.Routes.ItemRoutes import item_ns
from app.Routes.RestockLogRoutes import restock_ns
from app.Routes.ConsumptionLogRoutes import consumption_ns

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "mysql+mysqlconnector://root:@localhost:3306/KitchenSyncDB"

app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900  # 15 min
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 604800  # 7 days

db.init_app(app)
jwt = JWTManager(app)
api = Api(app, doc="/docs", title="KitchenSync API", version="1.0", description="Kitchen inventory management API")
api.add_namespace(auth_ns)
api.add_namespace(kitchen_ns)
api.add_namespace(item_ns)
api.add_namespace(restock_ns)
api.add_namespace(consumption_ns)

with app.app_context():
    try:
        db.engine.connect()
        print("✅ Connected successfully")
    except Exception as e:
        print("❌ Connection failed:", e)
    db.create_all()
