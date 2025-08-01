from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

# from db.db import db
from db import db
from models import ItemModel
from resources.schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request_data):
        item = ItemModel(**request_data) 
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, description="An error occurred while inserting the item.")
        
        return item
    
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}, 200
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, request_data, item_id):
        
        item = ItemModel.query.get(item_id)
        if item:
            item.price = request_data.get('price', item.price)
            item.name = request_data.get('name', item.name)
        else:
            item = ItemModel(id=item_id, **request_data)
        db.session.add(item)
        db.session.commit()
        return item
    
    