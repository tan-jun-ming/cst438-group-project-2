import json

from flask import request, Response
from app import app

import auth
import products

def error_401(message=None):
    ret = {"error": "401 Unauthorized"}
    if message:
        ret["message"] = message

    return Response(json.dumps(ret), status=401, mimetype="application/json")

def error_403(message=None):
    ret = {"error": "403 Forbidden"}
    if message:
        ret["message"] = message

    return Response(json.dumps(ret), status=403, mimetype="application/json")

@app.route("/api/login", methods=["POST"])
def login():
    login_details = request.get_json(force=True, silent=True)
    if not login_details:
        return error_401()
    username = login_details.get("username")
    password = login_details.get("password")

    if not username or not password:
        return error_401()

    return auth.login(username, password)

@app.route("/api/create_account", methods=["POST"])
def create_account():
    account_details = request.get_json(force=True, silent=True)
    if not account_details:
        return error_401()
    username = account_details.get("username")
    password = account_details.get("password")
    firstname = account_details.get("firstname")
    lastname = account_details.get("lastname")

    if not username or not password or not firstname or not lastname:
        return error_401()
        
    return auth.create(username, password, firstname, lastname)

@app.route("/api/product/<int:product_id>/cart", methods=["POST", "PUT", "PATCH"])
def add_to_cart(product_id):
    return products.add_to_cart(request.headers, product_id=product_id, params=request.get_json(force=True, silent=True))

@app.route("/api/product", methods=["POST"])
def add_product():
    return products.add_product(request.headers, params=request.get_json(force=True, silent=True))
