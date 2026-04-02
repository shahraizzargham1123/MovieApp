from flask_sqlalchemy import SQLAlchemy
from models.movie_model import db  # same db instance

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    is_active = db.Column(db.Boolean, default=True)

    reviews = db.relationship("Review", backref="user", lazy=True)