import uuid
from flask import Flask, request, abort
from flask.views import MethodView
from flask_smorest import Blueprint, Api
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import StoreModel
from db.db import db
from resources.schemas import StoreSchema



blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        return stores
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, request_data):
        store = StoreModel(**request_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, description="Store with this name already exists.")
        except SQLAlchemyError:
            abort(500, description="An error occurred while inserting the store.")
        
        return store, 201

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
            
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200
