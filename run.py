import json

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import utils
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import SampleObject

@app.route('/')
def hello_world():
    return 'Hello, World!'

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

        return "Object added. ID: " + obj.o_id
    except Exception as e:
        return(utils.get_traceback(e))

@app.route('/database_test')
def database_test():
    ret = SampleObject.query.all()
    return Response(json.dumps([r.serialize() for r in ret]), mimetype="application/json")

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()