from flask import Flask, request, abort
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


app = Flask(__name__)

app.config['API_TITLE'] = 'Store REST API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)