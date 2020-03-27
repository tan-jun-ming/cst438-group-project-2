import json
import datetime

from flask import Flask, Response, request, render_template
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import User, Product, Cart

import utils
import api


@app.route("/")
@app.route("/home")
@app.route("/index")
def home_page():
    return render_template("index.html")


@app.route("/create_account")
def routeAccountCreate():
    return render_template("AccountCreate.html")


@app.route("/account")
def routeAccountInfo():
    return render_template("AccountInfo.html")


@app.route("/login")
def routeAccountLogin():
    return render_template("AccountLogin.html")


@app.route("/checkout")
def checkout_page():
    return render_template("checkout.html")


@app.route("/product")
def product_page():
    return render_template("Product.html")
