from marshmallow import Schema, fields


class PlanItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlanStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
class PlanTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()



class ItemSchema(PlanItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlanStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlanTagSchema()), dump_only=True)

class StoreSchema(PlanStoreSchema):
    items = fields.List(fields.Nested(PlanItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlanTagSchema()), dump_only=True)

class TagSchema(PlanTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlanStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlanItemSchema()), dump_only=True)

class ItemTagSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)

