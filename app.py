from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')
def hello():
    db.create_all()
    tag = Tag(name="mytag", color=69)
    tag2 = Tag(name="othertag", color=70)
    db.session.add(tag)
    db.session.commit()
    return {'tags': [tag_schema.dump(t) for t in tag.query.all()]}

if __name__ == '__main__':
    app.run()
