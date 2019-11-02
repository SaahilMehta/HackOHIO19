from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
db.create_all()
ma = Marshmallow(app)

@app.route('/')
def foo():
    p1 = Pin(title="foo", latitude=40, longitude=82)
    p2 = Pin(title="bar", latitude=82, longitude=40)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    return 'bar'

@app.route('/pins')
def get_pins():
    return {
        'pins': [pin_schema.dump(p) for p in Pin.query.all()]
    }

@app.route('/pins/<id>')
def get_pin(id):
    return pin_schema.dump(
        Pin.query.filter_by(id=id).first())

if __name__ == '__main__':
    app.run()
