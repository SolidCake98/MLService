from marshmallow import Schema, fields
import datetime as dt

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
    size_name = fields.String()
    
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

    since_created = fields.Method("get_days_since_created")

    def get_days_since_created(self, obj):
        t = ['hour', 'day', 'week', 'month', 'year']
        f = [ 
            lambda : (dt.datetime.now() - obj.date_load).seconds//3600,
            lambda : (dt.datetime.now() - obj.date_load).days,
            lambda : int((dt.datetime.now() - obj.date_load).days / 7),
            lambda : int((dt.datetime.now() - obj.date_load).days / 30),
            lambda : int((dt.datetime.now() - obj.date_load).days / 365.25)
        ]

        res = ""
        for i in range(len(t)):
            val = f[len(t) - i - 1]()
            if val > 0:
                if val == 1:
                    res = f"a {t[len(t) - i - 1]}"
                else:
                    res = f"{val} {t[len(t) - i - 1]}s"

                return res
        return 'now'
                
        
