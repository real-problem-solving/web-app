# from db.db import db
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False, unique=False)
    store = db.relationship('StoreModel', back_populates= 'items')
    tags = db.relationship('TagModel', back_populates='items', secondary='items_tags')
    