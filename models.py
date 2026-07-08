from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(300), nullable=False)
    author = db.Column(db.String(200))
    image = db.Column(db.String(500))
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    genre = db.Column(db.String(100))
    image = db.Column(db.String(500))