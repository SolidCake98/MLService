from marshmallow import Schema, fields

class UserSchema(Schema):
    id          = fields.Int(dump_only=True)
    username    = fields.String()
    email       = fields.String()
    password    = fields.String()
    date_joined = fields.DateTime(dump_only=True)
    last_login  = fields.DateTime(dump_only=True)

class GroupSchema(Schema):
    id   = fields.Int(dump_only=True)
    name = fields.String()

class UserGroupSchema(Schema):
    id    = fields.Int(dump_only=True)
    user  = fields.Nested(UserSchema)
    group = fields.Nested(GroupSchema)

class DataSetMetaSchema(Schema):
    id   = fields.Int(dump_only=True)
    path = fields.String()
    size = fields.Int()
    type = fields.String()

class TagSchema(Schema):
    id       = fields.Int(dump_only=True)
    tag_name = fields.String()
    

class DataSetSchema(Schema):
    id          = fields.Int(dump_only=True)
    title       = fields.String()
    description = fields.String()
    date_load   = fields.DateTime()
    rating      = fields.Int()

    user        = fields.Nested(UserSchema)
    meta        = fields.Nested(DataSetMetaSchema)


class DataSetTagSchema(Schema):
    id      = fields.Int(dump_only=True)

    dataset = fields.Nested(DataSetSchema)
    tag     = fields.Nested(TagSchema)
