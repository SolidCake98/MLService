from marshmallow import Schema, fields
import datetime as dt

def day_since(date):
    t = ['hour', 'day', 'week', 'month', 'year']
    f = [ 
        lambda : (dt.datetime.now() - date).seconds//3600,
        lambda : (dt.datetime.now() - date).days,
        lambda : int((dt.datetime.now() - date).days / 7),
        lambda : int((dt.datetime.now() - date).days / 30),
        lambda : int((dt.datetime.now() - date).days / 365.25)
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


class GroupSchema(Schema):
    id   = fields.Int(dump_only=True)
    name = fields.String()


class UserGroupsSchema(Schema):
    id    = fields.Int(dump_only=True)
    group = fields.Nested(GroupSchema)


class UserSchema(Schema):
    id          = fields.Int(dump_only=True)
    username    = fields.String()
    email       = fields.String()
    password    = fields.String()
    date_joined = fields.DateTime(dump_only=True)
    last_login  = fields.DateTime(dump_only=True)

    since_join  = fields.Method("get_days_since_join")
    since_login = fields.Method("get_days_since_login")

    def get_days_since_join(self, obj):
        return day_since(obj.date_joined)

    def get_days_since_login(self, obj):
        if not obj.last_login:
            return 'None'
        return day_since(obj.last_login)


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

class DataSetTagSchema(Schema):
    id  = fields.Integer()
    tag = fields.Nested(TagSchema)

class DataSetSchema(Schema):
    id          = fields.Int(dump_only=True)
    name        = fields.String()
    title       = fields.String()
    description = fields.String()
    date_load   = fields.DateTime()
    rating      = fields.Float()

    user         = fields.Nested(UserSchema, only=('id', 'username'))
    dataset_meta = fields.Nested(DataSetMetaSchema)

    file_types   = fields.Nested(DataSetTypeSchema, many=True)
    tags         = fields.Nested(DataSetTagSchema, many=True)

    since_created = fields.Method("get_days_since_created")

    def get_days_since_created(self, obj):
        return day_since(obj.date_load)
                
        
class CountDataSetSchema(Schema):
    id       = fields.Int(dump_only=True)
    username = fields.String()
    count    = fields.Integer()
    avg      = fields.Float()
