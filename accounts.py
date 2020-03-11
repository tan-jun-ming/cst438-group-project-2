import api
import json

def login(username, password):
    valid = True
    if not valid:
        return api.error_401()

    return f"Logged in as {username} (This line won't be here in prod)\n" + json.dumps({"token": "insert token here"})

def create(username, password, firstname, lastname):
    if not validate_password(password):
        return api.error_401()
    
    return f"Account created (not really): {firstname}, {lastname}", 200

def validate_password(password):
    return True