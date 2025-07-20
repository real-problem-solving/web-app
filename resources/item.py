import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db.db import items

from resources.schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request_data):
         
        for item in items.values():
            if item['name'] == request_data['name'] and item['store_id'] == request_data['store_id']:
                abort(400, description="Item already exists in this store")

        item_id = str(uuid.uuid4().hex)
        item = {**request_data, "id": item_id}
        items[item_id] = item
        return item
    
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, description="Item not found")
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, description="Item not found")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, request_data, item_id):
        
        try:
            item = items[item_id]
            item |= (request_data)
            return item
        except KeyError:
            abort(404, description="Item not found")
    
    