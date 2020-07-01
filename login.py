from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import Model
#from flask_migrate import Migrate


app =  Flask(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

      