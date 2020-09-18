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