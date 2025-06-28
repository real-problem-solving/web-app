from flask import Flask, request
import psycopg2

app = Flask(__name__)

stores = [{"name": "My store", "items": [{"name": "My item", "price": 15.99}]}]
@app.get('/store')
def get_store():
    return {"stores": stores}
@app.post('/store')
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
        
    return {"store": new_store, "message": "Store created successfully"}, 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)