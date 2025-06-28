from flask import Flask
import psycopg2

app = Flask(__name__)

stores = [{"name": "My store", "items": [{"name": "My item", "price": 15.99}]}]
@app.get('/store')
def get_store():
    return {"stores": stores}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)