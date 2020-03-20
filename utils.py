import traceback
import json
import os

def get_database_uri():
    ret = os.getenv("DATABASE_URL")
    
    fp = "config.json"
    if not ret and os.path.isfile(fp):
        with open(fp, encoding="utf8") as o:
            config = json.loads(o.read())

        ret = config.get("DATABASE_URI")
    
    return ret

def get_jwt_secret():
    ret = os.getenv("JWT_SECRET")
    
    fp = "config.json"
    if not ret and os.path.isfile(fp):
        with open(fp, encoding="utf8") as o:
            config = json.loads(o.read())

        ret = config.get("JWT_SECRET")
    
    return ret

def get_traceback(e):
    return "".join(traceback.TracebackException.from_exception(e).format())