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
    user  = fields.Nested(UserSchema)
    group = fields.Nested(GroupSchema)


class DataSetMetaSchema(Schema):
    id   = fields.Int(dump_only=True)
    path = fields.String()
    size = fields.Int()
    type = fields.String()
    
class FileTypeSchema(Schema):
    type_name = fields.String()

class DataSetTypeSchema(Schema):
    file_type = fields.Nested(FileTypeSchema)

class TagSchema(Schema):
    id = fields.Integer()
    tag_name = fields.String()

class DataSetSchema(Schema):
    id          = fields.Int(dump_only=True)
    name        = fields.String()
    title       = fields.String()
    description = fields.String()
    date_load   = fields.DateTime()
    rating      = fields.Int()

    user         = fields.Nested(UserSchema, only=('id', 'username', 'last_login'))
    dataset_meta = fields.Nested(DataSetMetaSchema)

    file_types   = fields.Nested(DataSetTypeSchema, many=True)
    tags         = fields.Nested(TagSchema, many=True)

