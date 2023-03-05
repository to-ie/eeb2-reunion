from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from time import time
import jwt
from app import app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=False)
    section = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), index=True, unique=False)
    rsvp = db.Column(db.String(64), index=True, unique=False)
    avatar = db.Column(db.String(64), index=True, unique=False)
    currentlocation = db.Column(db.String(64), index=True, unique=False)
    verified = db.Column(db.String(64), index=True, unique=False)
    
    facebook = db.Column(db.String(64), index=True, unique=False)
    twitter = db.Column(db.String(64), index=True, unique=False)
    instagram = db.Column(db.String(64), index=True, unique=False)
    linkedin = db.Column(db.String(64), index=True, unique=False)
    snapchat = db.Column(db.String(64), index=True, unique=False)
    reddit = db.Column(db.String(64), index=True, unique=False)
    mastodon = db.Column(db.String(64), index=True, unique=False)
    tiktok = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    section = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    registered = db.Column(db.String(120), index=True, unique=False)
    rsvp = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '{}'.format(self.name)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '{}'.format(self.section)
