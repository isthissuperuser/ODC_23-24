from . import app
from functools import wraps
from flask import request, session, render_template, redirect, url_for, flash
from .db import User, db
import logging
import os
from string import ascii_letters
import subprocess
from .parser import validate_file

l = logging.getLogger('pyb.views')
l.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
last_cleanup = None

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'username' not in session:
            flash("You need to login!", 'info')
            return redirect(url_for('login'))
        return f(*args, **kws)
    return decorated_function

def delete_obj(o):
    db.session.delete(o)

@app.route('/pybook', methods=['GET'])
@authorize
def pybook():
    return render_template("book.html")


@app.route('/run', methods=['POST'])
@authorize
def run():
    code = request.data
    l.debug("RUN request: %r, %r", request, code)
    path = os.path.join("/tmp", "%s.py" % session['username'])
    with open(path, "wb") as f:
        f.write(code)
    if not validate_file(path):
        return "Unallowd Code!"
    # p1 = subprocess.Popen('python %s' % path, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out, err = p1.communicate()
    try:
        out = subprocess.check_output('python %s' % path, shell=True, stderr=subprocess.STDOUT, timeout=1)
        return out
    except subprocess.TimeoutExpired as e:
        return "TimeOut!"
    return "Unknown Problem!"

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
        db.session.add(u)
        db.session.commit()
        session['username'] = username
        flash("Registration completed!", 'success')
        return redirect(url_for('login'))
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
        return redirect(url_for('pybook'))
    flash("login failed!", 'danger')
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return "Logout succesful!", 200

@app.route('/')
def redirect_view():
    return redirect('/pybook')