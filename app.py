import json

from flask import Flask, Response, request, render_template
from flask_sqlalchemy import SQLAlchemy

import utils
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import SampleObject

@app.route('/')
@app.route('/home')
@app.route('/index')
def home_page():
    return render_template("index.html")

@app.route('/hello')
def route_two():
    return 'Hello, this is another route!'

@app.route('/database_test/add')
def database_test_add():
    o_name = request.args.get('name')
    o_num = request.args.get('num')
    o_bool = request.args.get('bool')

    try:
        o_bool = bool(int(o_bool))
    except:
        o_bool = False

    try:
        o_num = float(o_num)
    except:
        o_num = 0

    try:
        obj = SampleObject(o_name, o_num, o_bool)
        db.session.add(obj)
        db.session.commit()

        return f"Object added. ID: {obj.o_id}"
    except Exception as e:
        return Response(utils.get_traceback(e), mimetype="text/plain")

@app.route('/database_test')
def database_test():
    try:
        ret = SampleObject.query.all()
        return Response(json.dumps([r.serialize() for r in ret]), mimetype="application/json")
    except Exception as e:
        return Response(utils.get_traceback(e), mimetype="text/plain")