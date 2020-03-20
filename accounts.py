import api
import hashlib
import json
import datetime
import random
import jwt

import utils
from flask import Response
from app import db
from models import User
from config import Config

def login(username, password):
    valid = True
    if not valid:
        return api.error_401()

    return f"Logged in as {username} (This line won't be here in prod)\n" + json.dumps({"token": "insert token here"})

def create(username, password, firstname, lastname):
    if not validate_password(password):
        return api.error_401("Invalid password.")
    
    user = User.query.filter_by(username=username)
    if user.count():
        return api.error_403("This username already exists.")
    
    ts = datetime.datetime(1970, 1, 1)
    password_salt = generate_salt()
    password_hash = hash_password(password.encode("utf-8"), password_salt)

    try:
        new_user = User(username, firstname, lastname, password_hash, password_salt, ts)
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        return Response(utils.get_traceback(e),status=500, mimetype="text/plain")
    

    return Response(json.dumps(
        {
            "message": "Account created successfully",
            "user_id": new_user.user_id,
            "username": username,
            "firstname": firstname,
            "lastname": firstname
        
        }), mimetype="application/json"), 200

def validate_password(password):
    return True

def hash_password(password, salt):
    return hashlib.scrypt(password, salt=salt, n=16, r=16, p=16)

def generate_salt(length=64):
    return bytes([random.randint(0, 255) for i in range(length)])

def generate_token(user_id, timestamp=None):
    if timestamp == None:
        timestamp = datetime.datetime.utcnow()
    
    secret = Config._jwt_secret