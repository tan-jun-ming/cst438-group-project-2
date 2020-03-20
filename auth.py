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
    user = User.query.filter_by(username=username)

    if not user.count():
        return api.error_403("This username does not exist.")
    
    user = user.one()

    password_hash = hash_password(password.encode("utf-8"), user.password_salt)

    if password_hash != user.password_hash:
        return api.error_401("Invalid password.")

    new_token = generate_token(user.user_id)

    payload = json.dumps(
        {
            **user.serialize(),
            **{"token": new_token}
        }
    )

    return Response(payload, mimetype="application/json")


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
            "lastname": lastname
        
        }), mimetype="application/json")

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
    payload = {
        "user_id": user_id,
        "timestamp": timestamp.timestamp()
        }

    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')

    return encoded_jwt.decode("utf-8")

def invalidate_past_tokens(user_id, timestamp=None):
    if timestamp == None:
        timestamp = datetime.datetime.utcnow()

    user = User.query.filter_by(user_id=user_id)

    if not user.count():
        raise ValueError("User ID does not exist.")

    user.one().oldest_valid_timestamp = timestamp
    db.session.commit()

    return True

def validate_token(token):
    secret = Config._jwt_secret

    try:
        decoded_jwt = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        return False
    
    user_id = decoded_jwt.get("user_id")
    timestamp = decoded_jwt.get("timestamp")

    if not user_id or not timestamp:
        return False
    
    user = User.query.filter_by(user_id=user_id)

    if not user.count():
        return False
    
    user = user.one()
    if timestamp < user.oldest_valid_timestamp.timestamp():
        return False
    
    return user.serialize()


def set_user_admin_status(user_id, status):
    user = User.query.filter_by(user_id=user_id)

    if not user.count():
        return False
    
    user = user.one()
    user.is_admin = status

    db.session.commit()
    return True




def token_precheck(func):
    def wrapper(headers, **kwargs):
        token = headers.get("Authorization")
        if not token:
            return api.error_401()
        
        user = validate_token(token)

        if not user:
            return api.error_401()
        
        result = func(user, **kwargs)

        return result

    return wrapper

def admin_precheck(func):
    def wrapper(user, **kwargs):

        if not user["is_admin"]:
            return api.error_403()
        
        result = func(user, **kwargs)

        return result

    return wrapper
