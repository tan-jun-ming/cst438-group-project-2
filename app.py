import json
import datetime

from flask import Flask, Response, request, render_template
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User, Product, Cart

import utils
import api


@app.route('/')
@app.route('/home')
@app.route('/index')
def home_page():
    return render_template("index.html")

@app.route('/hello')
def route_two():
    return 'Hello, this is another route!'
	
@app.route('/create_account')
def routeAccountCreate():
	return render_template("AccountCreate.html")

@app.route('/account')
def routeAccountInfo():
	return render_template("AccountInfo.html")
	
@app.route('/login')
def routeAccountLogin():
	return render_template("AccountLogin.html")

@app.route('/database_test/add_user')
def database_test_add_user():
    username = request.args.get('username')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    try:
        obj = User(username, first_name, last_name, 1, 1, datetime.datetime.utcnow())
        db.session.add(obj)
        db.session.commit()

        return f"Object added. ID: {obj.user_id}"
    except Exception as e:
        return Response(utils.get_traceback(e), mimetype="text/plain")

@app.route('/database_test/add_product')
def database_test_add_product():
    product_id = request.args.get('product_id')
    name = request.args.get('name')
    details = request.args.get('details')
    image_url = request.args.get('image_url')
    price = request.args.get('price')

    try:
        obj = Product(name, details, image_url, price)
        db.session.add(obj)
        db.session.commit()

        return f"Object added. ID: {obj.product_id}"
    except Exception as e:
        return Response(utils.get_traceback(e), mimetype="text/plain")

@app.route('/database_test/add_cart')
def database_test_add_cart():
    product_id = request.args.get('product_id')
    user_id = request.args.get('user_id')
    amount = request.args.get('amount')

    try:
        obj = Cart(product_id, user_id, 1)
        db.session.add(obj)
        db.session.commit()

        return f"Object added. ID: {obj.user_id}"
    except Exception as e:
        return Response(utils.get_traceback(e), mimetype="text/plain")

@app.route('/database_test/remove_product')
def remove_product():
    product_id = request.args.get('product_id')

    try:
        obj = Product.query.filter_by(product_id=product_id).one()
        db.session.delete(obj)
        db.session.commit()

        return f"Object removed: ID = {product_id}"
    except Exception as e:
        return Response(utils.get_traceback(e), mimetype="text/plain")

@app.route('/database_test')
def database_test():
    try:
        retUser = User.query.all()
        retProduct = Product.query.all()
        retCart = Cart.query.all()

        ret = json.dumps([[r.serialize() for r in i] for i in [retUser, retProduct, retCart]])

        return Response(ret, mimetype="application/json")
    except Exception as e:
        return Response(utils.get_traceback(e), mimetype="text/plain")

@app.route('/checkout')
def checkout_page():
    return render_template("checkout.html")


@app.route('/product')
def product_page():
    return render_template("Product.html")