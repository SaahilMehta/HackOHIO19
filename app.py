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
    p1 = Pin(title="foo", latitude=40, longitude=82, category_id=2, map_id=1)
    p2 = Pin(title="bar", latitude=82, longitude=40, category_id=2, map_id=2)
    c1 = Category(name="Dog Friendly", color=0x800800, description="Parks and other locations that would be great to take your pet")
    c2 = Category(name="Study Locations", color=0x0000ff, description="Quiet spots to get work done")
    t1 = Tag(name='footag')
    t2 = Tag(name='bartag')
    t3 = Tag(name='foobartag')
    m1 = Map(name='fooMap', total_score = 50, color = 0x696969)
    m2 = Map(name='standardMap', color=9000, downvotes=100, upvotes=0)
    p1.tags.append(t1)
    p2.tags.append(t2)
    p2.tags.append(t3)
    
    db.session.add(m1)
    db.session.add(m2)
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(c1)
    db.session.add(c2)
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

@app.route('/pins/top')
def get_top_pins():
    return {
        'pins': [pin_schema.dump(p) for p in Pin.query.order_by(db.desc(Pin.total_score)).limit(10).all()]
    }

@app.route('/pins', methods=['POST'])
def new_pin():
    j = request.json
    p = Pin(creator_id=j['creator_id'] if j['creator_id'] else None,
        map_id=j['map_id'] if j['map_id'] else None,
        rating=j['rating'] if j['rating'] else None,
        title=j['title'] if j['title'] else None,
        description=j['description'] if j['description'] else None,
        latitude=j['latitude'] if j['latitude'] else None,
        longitude=j['longitude'] if j['longitude'] else None,
        datetime_posted=j['datetime_posted'] if j['datetime_posted'] else None,
        color=j['color'] if j['color'] else None)
    db.session.add(p)
    db.session.commit()
    return {'message': 'Pin was successfully created!'}

# @app.route('/pins', methods=['DELETE'])
# def del_pin(id)
#     Pin.query.filter_by(id=id).delete()
#     return {'message': 'Pin was successfully deleted'}

@app.route('/tags')
def get_tags():
    return {
        'tags': [tag_schema.dump(p) for p in Tag.query.all()]
    }

@app.route('/category')
def get_categories():
    return {
        'categories': [category_schema.dump(c) for c in Category.query.all()]
    }

@app.route('/category/<id>/pins')
def get_category_pins(id):
    return {
        'pins': [pin_schema.dump(p) for p in 
        db.session.query(Category).join(Pin).filter(Category.id == Pin.category_id).all()] 
    }
# # This one is hard
# @app.route('/tag/<id>/pins')
# def get_tag_pins(id):
#     return {
#         'pins': [pin_schema.dump(p) for p in 
#         Pin.query.filter(Pin.tags.any(id = id).all())
#     }

@app.route('/maps')
def get_maps():
    return {
        'maps': [map_schema.dump(m) for m in Map.query.all()]
    }

@app.route('/maps', methods=['POST'])
def new_map():
    j = request.json
    m = Map(creator_id=j['creator_id'] if j['creator_id'] else None,
        upvotes=j['upvotes'] if j['upvotes'] else None,
        downvotes=j['downvotes'] if j['downvotes'] else None,
        total_score=j['total_score'] if j['total_score'] else None,
        name=j['name'] if j['name'] else None,
        color=j['color'] if j['color'] else None,
    )
    db.session.add(m)
    db.session.commit()
    return {'message': 'Map was successfully created!'}

@app.route('/maps/<map_id>/pins')
def get_map_pins(map_id):
    return {
        'pins': [pin_schema.dump(p) for p in 
        db.session.query(Map).join(Pin).filter(Map.id == Pin.map_id).all()]
    }

@app.route('/creator/<creator_id>/pins')
def get_creator_pins(creator_id):
    return {
        'pins': [pin_schema.dump(p) for p in 
        db.session.query(Creator).join(Pin).filter(Creator.id == Pin.creator_id).filter_by(creator_id=creator_id)]
    }

@app.route('/creator/<creator_id>/maps')
def get_creator_maps(creator_id):
    return {
        'maps': [map_schema.dump(m) for m in 
        db.session.query(Creator).join(Map).filter(Creator.id == Map.creator_id).filter_by(creator_id=creator_id)]
    }

@app.route('/creator', methods=['POST'])
def new_creator():
    j = request.json
    c = Creator(name=j['name'] if j['name'] else None,
        total_score=j['total_score'] if j['total_score'] else None,
        password_hash=j['password_hash'] if j['password_hash'] else None,
    )
    db.session.add(c)
    db.session.commit()
    return {'message': 'Map was successfully created!'}

if __name__ == '__main__':
    app.run()
