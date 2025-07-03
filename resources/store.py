import uuid
from flask import Flask, request, abort
from flask.views import MethodView
from flask_smorest import Blueprint, Api
from db.db import stores



blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}, 200

    def post(self):
        request_data = request.get_json()
        if "name" not in request_data:
            abort(400, description="Bad Request: Missing required field 'name'")
        for store in stores.values():
            if store['name'] == request_data['name']:
                abort(400, description="Store already exists with this name")
        store_id = str(uuid.uuid4().hex)
        store = {**request_data, "id": store_id}
        stores[store_id] = store
        return store, 201

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            store = stores[store_id]
            return store, 200
        except KeyError:
            abort(404, description="Store not found")
            
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}, 200
        except KeyError:
            abort(404, description="Store not found")
