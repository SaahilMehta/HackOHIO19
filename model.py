from app import db
from app import ma
from sqlalchemy.orm import relationship

tags = db.Table('tags', db.Model.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('pin_id', db.Integer, db.ForeignKey('pin.id'), primary_key=True)
)

class Pin(db.Model):
    __tablename__ = 'pin'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    map_id = db.Column(db.Integer, db.ForeignKey('map.id'))
    rating = db.Column(db.Float)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(250))
    tags = db.relationship('Tag', secondary=tags)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    datetime_posted = db.Column(db.DateTime())
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    color = db.Column(db.Integer)    

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    color = db.Column(db.Integer)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    color = db.Column(db.Integer)
    description = db.Column(db.String(250))

class Map(db.Model):
    __tablename__ = 'map'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    pins = relationship("Pin")
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    name = db.Column(db.String(40))
    color = db.Column(db.Integer)

class Creator(db.Model):
    __tablename__ = 'creator'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    total_score = db.Column(db.Integer)
    name = db.Column(db.String(40))
    password_hash = db.Column(db.String(40))

class PinSchema(ma.ModelSchema):
    class Meta:
        model = Pin

class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag

class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category

class MapSchema(ma.ModelSchema):
    class Meta:
        model = Map

class CreatorSchema(ma.ModelSchema):
    class Meta:
        model = Creator

pin_schema = PinSchema()
tag_schema = TagSchema()
category_schema = CategorySchema()
map_schema = MapSchema()
creator_schema = CreatorSchema()
db.create_all()