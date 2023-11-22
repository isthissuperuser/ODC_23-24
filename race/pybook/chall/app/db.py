from . import app
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha3_256
from config import DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def verify_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        if h == self.password:
            return True
        return False

    def set_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        self.password = h

class Script(db.Model):
    __tablename__ = 'scripts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('scripts', lazy=True))
    path = db.Column(db.String(120), unique=False, nullable=False)


    def __repr__(self):
        return '<Script [%r, %d] %s >' % (self.id, self.user_id, self.path)

