from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
db = SQLAlchemy(app)

from app import routes
