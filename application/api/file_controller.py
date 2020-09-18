from flask_restful import Resource, reqparse
import werkzeug

class FileApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('fil', type=werkzeug.datastructures.FileStorage, location='files')
        self.parser.add_argument('rr',  type=int)
    
    def post(self):
        args = self.parser.parse_args()
        file = args['fil']
        i = args['rr']    
        return {'data' : file.filename, 'i': i}

    def get(self):
        return {'hello': 'world'}

