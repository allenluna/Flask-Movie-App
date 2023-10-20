from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import Relationship
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    movies = Relationship("Movies", back_populates="user_name")
    mylists = Relationship("Mylist", back_populates="user_name")

class Movies(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    overview = db.Column(db.String)
    banner = db.Column(db.String)
    image = db.Column(db.String)
    movie = db.Column(db.String)
    key = db.Column(db.String)
    reviews = db.Column(db.String)
    author_review = db.Column(db.String)
    date = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_name = Relationship("User", back_populates="movies")


class Popular(db.Model):
    __tablename__ = "populars"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    overview = db.Column(db.String)
    banner = db.Column(db.String)
    image = db.Column(db.String)
    movie = db.Column(db.String)
    key = db.Column(db.String)
    reviews = db.Column(db.String)
    author_review = db.Column(db.String)
    date = db.Column(db.String)

class Upcomming(db.Model):
    __tablename__ = "upcommings"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    overview = db.Column(db.String)
    banner = db.Column(db.String)
    image = db.Column(db.String)
    movie = db.Column(db.String)
    key = db.Column(db.String)
    reviews = db.Column(db.String)
    author_review = db.Column(db.String)
    date = db.Column(db.String)

class Cast(db.Model):
    __tablename__ = "casts"
    id = db.Column(db.Integer, primary_key=True)
    cast_id = db.Column(db.Integer)
    name = db.Column(db.String)
    cast_img = db.Column(db.String)


class Mylist(db.Model):
    __tablename__ = "mylists"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    overview = db.Column(db.String)
    banner = db.Column(db.String)
    image = db.Column(db.String)
    movie = db.Column(db.String)
    key = db.Column(db.String)
    reviews = db.Column(db.String)
    author_review = db.Column(db.String)
    date = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_name = Relationship("User", back_populates="mylists")




