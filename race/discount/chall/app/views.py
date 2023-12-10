import logging
import os
import random
import string
import subprocess
import json
from functools import wraps
from string import ascii_letters
from sqlalchemy import exists
from flask import flash, redirect, render_template, request, session, url_for

from . import app
from .db import Cart, DiscountCode, Item, User, db
from .parser import validate_file

l = logging.getLogger('discount.views')
l.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
last_cleanup = None

def random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'username' not in session:
            flash("You need to login!", 'info')
            return redirect(url_for('login'))
        return f(*args, **kws)
    return decorated_function


@app.before_first_request
def load_db():
    app.logger.info("loading the db")
    with open('../flag') as flag_file:
        flag = flag_file.read()
    with open('items.json') as json_file:
        data = json.load(json_file)
        for item in data:
            record = db.session.query(Item).filter(Item.name == item['name']).first()
            if record is None:
                description = item['description']
                if 'flag' in item['name'].lower():
                    description = flag
                record = Item(name=item['name'], price=int(item['price'])*100, description=description)
                db.session.add(record)
        db.session.commit()

def delete_obj(o):
    db.session.delete(o)

@app.context_processor
def context_functions():
    def get_money():
        u = User.query.filter_by(username=session['username']).first()
        if u is None:
            return 0
        return u.money
    def get_cart():
        u = User.query.filter_by(username=session['username']).first()
        if u is None:
            return []
        c = Cart.query.filter_by(user_id=u.id).first()
        if c is None:
            return []
        return c.items
    def get_items():
        u = User.query.filter_by(username=session['username']).first()
        if u is None:
            return []
        return u.items
    return dict(user_money=get_money, user_cart=get_cart, user_items=get_items)

@app.route('/items', methods=['GET'])
@authorize
def items():
    u = User.query.filter_by(username=session['username']).first()
    if u is None:
        return redirect(url_for('login'))
    return render_template("items.html", items=u.items)


@app.route('/shop', methods=['GET'])
@authorize
def shop():
    items = db.session.query(Item).all() 
    return render_template("shop.html", items=items)

@app.route('/cart', methods=['GET'])
@app.route('/cart/<string:pay>', methods=['GET'])
@authorize
def cart(pay=None):
    u = User.query.filter_by(username=session['username']).first()
    cart = db.session.query(Cart).filter(Cart.user_id == u.id).first()
    l.debug("Cart request: %r", cart)
    if cart is None:
        d = DiscountCode.query.filter_by(user_id=u.id).first()
        if d is not None:
            flash("You still have a discount code!: %s" % d.code, 'warning')
        return render_template("cart.html", items=[], total=0, discount=0)
    discount = cart.discount_rate
    total = 0
    for item in cart.items:
        total += int(item.price * (100 - discount)/100)
    if pay is None:
        d = DiscountCode.query.filter_by(user_id=u.id).first()
        if d is not None:
            flash("You still have a discount code!: %s" % d.code, 'warning')
        return render_template("cart.html", items=cart.items, total=total, discount=discount)

    if u.money < total:
        flash("Not enough money!", 'danger')
        return redirect(url_for('cart'))
    # pay the money
    u.money -= total
    # add the items to the user
    for item in cart.items:
        u.items.append(item)
    # delete the cart
    db.session.delete(cart)
    db.session.commit()
    flash("Payment was sucessful!", 'success')
    return redirect(url_for('items'))


@app.route('/add_to_cart', methods=['GET'])
def add_to_cart():
    item_id = request.args.get('item_id')
    l.debug("Add to cart request: %r", item_id)
    u = User.query.filter_by(username=session['username']).first()
    if u is None:
        return redirect(url_for('shop'))
    i = Item.query.filter_by(id=item_id).first()
    if i is None:
        flash("Item not found!", 'danger')
        return redirect(url_for('shop'))
    c = Cart.query.filter_by(user_id=u.id).first()
    if c is None:
        c = Cart(user_id=u.id, discount_rate = 0)
        db.session.add(c)

    l.debug("Adding item %r to cart %r", i, c)
    c.items.append(i)
    l.debug("items: %r", c.items)
    db.session.commit()
    flash("Item added to the Cart!", 'success')
    return redirect(url_for('shop'))


@app.route('/apply_discount', methods=['POST'])
def apply_discount():
    l.debug("Apply Discount request: %r, %r", request, request.form)
    discountcode = request.form['discount'].strip()
    u = User.query.filter_by(username=session['username']).first()
    if u is None:
        return redirect(url_for('login'))
    c = Cart.query.filter_by(user_id=u.id).first()
    if c is None:
        flash("Cart not found!", 'danger')
        return redirect(url_for('shop'))
    d = DiscountCode.query.filter_by(code=discountcode).first()
    if d is None:
        flash("Discount code not found!", 'danger')
        return redirect(url_for('cart'))
    if d.user != u:
        flash("Discount code not for you!", 'danger')
        return redirect(url_for('cart'))
    # apply discount
    c = Cart.query.filter_by(user_id=u.id).first()
    l.debug("Before Discount rate: %r", c.discount_rate)
    c.discount_rate += d.discount_rate
    db.session.commit()
    l.debug("After Discount rate: %r", c.discount_rate)
    flash("Discount code applied!", 'success')

    # delete discount code, after this it can't be used again
    delete_obj(d)
    db.session.commit()

    return redirect(url_for('cart'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    l.debug("Register request: %r, %r", request, request.form)
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    if username == "" or password == "":
        l.debug("invalid username or password: %s:%s", username, password)
        flash("username or password invalid!", 'danger')
        return redirect(url_for('register'))
    for c in username:
        if c not in ascii_letters:
            l.debug("invalid characters in username: %s", username)
            flash("invalid characters in username!", 'danger')
            return redirect(url_for('register'))

    u = User.query.filter_by(username=username).first()
    if u is None:
        l.debug("New User, %s:%s", username, password)
        u = User(username=username)
        u.set_password(password)
        u.money = 500
        db.session.add(u)
        db.session.commit()
        discount_string = random_string(10)
        discount = DiscountCode(code=discount_string, user_id=u.id, discount_rate=50)
        l.debug("New DiscountCode: %r", discount)
        db.session.add(discount)
        db.session.commit()
        session['username'] = username
        flash("Registration completed!", 'success')
        flash("Use your discount code! Code: %s" % discount_string, 'warning')
        return redirect(url_for('shop'))
    flash("Username already exists!", 'info')
    return redirect(url_for('register'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    session.clear()
    l.debug("Login request: %r, %r", request, request.form)
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    u = User.query.filter_by(username=username).first()
    if u is not None and u.verify_password(password):
        l.debug("Logged in, %s:%s", username, password)
        session['username'] = username
        flash("Welcome back!", 'success')
        return redirect(url_for('shop'))
    flash("login failed!", 'danger')
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("Logout succesful!", 'success')
    return redirect('/login')

@app.route('/home')
@app.route('/')
def home():
    return redirect('/shop')