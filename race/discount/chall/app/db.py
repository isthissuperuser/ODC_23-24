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
    money = db.Column(db.Integer, unique=False, nullable=False)
    items = db.relationship('Item', secondary='user_items', backref=db.backref('user', lazy=True))

    user_items = db.Table('user_items', db.Model.metadata,
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
    )

    def __repr__(self):
        return '<User %r, items:%d>' % (self.username, len(self.items))

    def verify_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        if h == self.password:
            return True
        return False

    def set_password(self, password):
        h = sha3_256(password.encode('utf-8')).hexdigest()
        self.password = h


class DiscountCode(db.Model):
    __tablename__ = 'discount_codes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(120), unique=True, nullable=False)
    discount_rate = db.Column(db.Integer, unique=False, nullable=False)
    user = db.relationship('User', backref=db.backref('discount_codes', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<DiscountCode %r %d>' % (self.code, self.discount_rate)

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart', lazy=True))
    items = db.relationship('Item', secondary='cart_items', backref=db.backref('carts', lazy=True))
    discount_rate = db.Column(db.Integer, unique=False, nullable=False)

    cart_items = db.Table('cart_items', db.Model.metadata,
        db.Column('cart_id', db.Integer, db.ForeignKey('carts.id')),
        db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
    )

    def __repr__(self):
        return '<Cart [%r, %d] %d >' % (self.id, len(self.items), self.discount_rate)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.Integer , unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)

    def __repr__(self):
        return '<Item [%r, %d] %s >' % (self.id, self.price, self.name)

