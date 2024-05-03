import json
import os
from datetime import datetime, timedelta

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel


import requests
from flask import Flask, render_template, redirect, url_for, flash, abort, request, current_app, jsonify, make_response, \
    Response
from sqlalchemy.orm import joinedload

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)
babel = Babel(app)


@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table
    user = User.query.get(int(user_id))
    if user:
        return user
    # If not, check if user is in free_user table

    # If user is not in either table, return None
    return None


app.config['BABEL_DEFAULT_LOCALE'] = 'en'

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


with app.app_context():




    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        email = db.Column(db.String(100))
        country = db.Column(db.String(100))
        subscription = db.Column(db.String(100))
        credit = db.Column(db.Integer)

        role = db.Column(db.String(100), default="user")
        pay = db.Column(db.Boolean(), default=False)
        message = db.Column(db.String(1000))
        starting_day = db.Column(db.DateTime)
        due_Date = db.Column(db.DateTime)
        delegate = db.Column(db.DateTime)
    db.create_all()


class MyModelView(ModelView):
    def is_accessible(self):
        return True


admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
@app.route("/")
def start():
    return render_template("index.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        phone=request.form.get("phone")
        password=request.form.get("password")
        user=User.query.filter_by(phone=phone).first()
        if user and user.password==password:
            login_user( user)
            return redirect("/")
        else:
            return "somthing went wrong"
    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        phone=request.form.get("phone")
        password=request.form.get("password")
        user=User(phone=phone,password=password,role="user")
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)
