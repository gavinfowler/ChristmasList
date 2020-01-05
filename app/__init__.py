from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(
    __name__, static_folder="../client/dist/", template_folder="../client/dist/",
)
app.config.from_object(Config)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

from app import routes, models

if Config.DB_SETUP == "0":
    has_admin = len(models.User.query.filter_by(is_admin=True).all()) > 0
    if not has_admin:
        email = Config.ADMIN_EMAIL
        password = Config.ADMIN_PASSWORD
        adminUser = models.User(
            name="admin", username="admin", email=email, is_admin=True
        )
        adminUser.set_password(password)
        db.session.add(adminUser)
        db.session.commit()
        has_admin = models.User.query.filter_by(is_admin=True).all()

