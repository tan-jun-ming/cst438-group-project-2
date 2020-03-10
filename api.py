from flask import request
from app import app

import accounts

def error_401():
    return "401 Unauthorized", 401

@app.route("/api/login", methods=["POST"])
def login():
    login_details = request.get_json(force=True, silent=True)
    if not login_details:
        return error_401()
    username = login_details.get("username")
    password = login_details.get("password")

    if not username or not password:
        return error_401()

    return accounts.login(username, password)

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
        
    return accounts.create(username, password, firstname, lastname)