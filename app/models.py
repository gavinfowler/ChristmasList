from datetime import datetime
from flask import jsonify
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    family_id = db.Column(db.Integer, db.ForeignKey("family.id"), nullable=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_posts(self):
        posts = Post.query.filter_by(user_id=self.id).all()
        return posts

    def set_family(self, family_id):
        self.family_id = family_id
        return self.family_id

    def serialize(self):
        user = {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "family_id": self.family_id,
        }
        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    notes = db.Column(db.String(1000))
    item_url = db.Column(db.String(500))
    img_url = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def serialize(self):
        post = {
            "title": self.title,
            "notes": self.notes,
            "img_url": self.img_url,
            "item_url": self.item_url,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "id": self.id,
        }
        return post

    def __repr__(self):
        return '<Post "{}" User "{}">'.format(
            self.title, load_user(self.user_id).username
        )


class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    key = db.Column(db.Integer, index=True, unique=True)
    creator = db.Column(db.String(64), unique=True)
    # creator = db.relationship(db.Integer, db.ForeignKey("User.id"))
    users = db.relationship("User", backref="member", lazy=True)

    def serialize(self):
        family = {
            "id": self.id,
            "name": self.name,
            "key": self.key,
            "creator": self.creator,
        }
        return family

    def __repr__(self):
        return '<Family "{}" id "{}">'.format(self.name, self.id)
