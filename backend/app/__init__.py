from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create flask application instance
app = Flask(__name__)

# load config file
app.config.from_pyfile("config.py")

# initialize SQLAlchemy
db = SQLAlchemy(app)

# create login manager
login_manager = LoginManager(app)

# import routes
from app import routes

# register database models
from app.models import User, Expense

# create database tables
with app.app_context():
    db.create_all()