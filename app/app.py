import uuid
from db.db import stores, items
from flask import Flask, request, abort
# from flask_smorest import abort
import psycopg2

app = Flask(__name__)



@app.get('/store')
def get_stores():
    return {"stores": list(stores.values())}, 200
    # return {"stores": stores}, 200

@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        store = stores[store_id]
        return store, 200
    except KeyError:
        abort(404, description="Store not found")

@app.post('/store')
def create_store():
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

@app.post('/item')
def create_item():
    request_data = request.get_json()

    if ("price" not in request_data or "store_id" not in request_data 
        or "name" not in request_data):
        abort (400, description="Bad Request: Missing required fields: price, store_id, name")
    for item in items.values():
        if item['name'] == request_data['name'] and item['store_id'] == request_data['store_id']:
            abort(400, description="Item already exists in this store")

    item_id = str(uuid.uuid4().hex)
    item = {**request_data, "id": item_id}
    items[item_id] = item
    return item, 201

@app.get('/items')
def get_items():
    return {"items": list(items.values())}, 200

@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort (404, description="Item not found")
@app.put('/item/<string:item_id>')
def update_item(item_id):
    request_data = request.get_json()
    if "name" not in request_data or "price" not in request_data:
        abort(400, description="Bad Request: Missing required fields 'name' or 'price'")
    
    try:
        item = items[item_id]
        item |= (request_data)
        return item, 200
    except KeyError:
        abort(404, description="Item not found")

@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted successfully"}, 200
    except KeyError:
        abort(404, description="Item not found")

@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted successfully"}, 200
    except KeyError:
        abort(404, description="Store not found")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)