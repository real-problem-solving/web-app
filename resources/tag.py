from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import StoreModel, TagModel, ItemModel
from resources.schemas import TagSchema, ItemTagSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, request_data, store_id):
        # store = StoreModel.query.get_or_404(store_id)
        # tag = TagModel(name=request_data['name'], store=store)
        if TagModel.query.filter(StoreModel.id == store_id, TagModel.name == request_data['name']).first():
            abort(409, message="A tag with that name already exists in this store.")
        tag = TagModel(**request_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, description="An error occurred while inserting the tag.", error=str(e))
        
        return tag


    
@blp.route('/item/<string:item_id>/tag/<string:tag_id>')
class LinkTagsToItem(MethodView):
    @blp.response(201, ItemTagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, description="An error occurred while linking the tag to the item.")
        return {"message": "Tag linked to item", "tag": tag, "item": item}
    
    @blp.response(200, ItemTagSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if tag in item.tags:
            item.tags.remove(tag)
            try:
                db.session.commit()
            except SQLAlchemyError:
                abort(500, description="An error occurred while unlinking the tag from the item.")
            return {"message": "Tag unlinked from item", "tag": tag, "item": item}
        else:
            abort(404, description="Tag not associated with this item.")

@blp.route('/tag/<string:tag_id>') 
class TagDelete(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(
        200,
        description="Tag deleted successfully",
        example={"message": "Tag deleted successfully"}
    )
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        400,
        description="Returned if the tag is associated to one or more items. In this case, the tag is not deleted.",
        example={"message": "Cannot delete tag with associated items or stores"})
    
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted successfully"}
        abort(
            400,
            description="Cannot delete tag with associated items or stores"
        )