import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db.db import items

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        request_data = request.get_json()

        if ("price" not in request_data or "store_id" not in request_data 
            or "name" not in request_data):
            abort(400, description="Bad Request: Missing required fields: price, store_id, name")
        
        for item in items.values():
            if item['name'] == request_data['name'] and item['store_id'] == request_data['store_id']:
                abort(400, description="Item already exists in this store")

        item_id = str(uuid.uuid4().hex)
        item = {**request_data, "id": item_id}
        items[item_id] = item
        return item
    
@blp.route("/item/<string:item_id>")
class Item(MethodView):
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
    
    def put(self, item_id):
        request_data = request.get_json()
        if "name" not in request_data or "price" not in request_data:
            abort(400, description="Bad Request: Missing required fields 'name' or 'price'")
        
        try:
            item = items[item_id]
            item |= (request_data)
            return item
        except KeyError:
            abort(404, description="Item not found")
    
    