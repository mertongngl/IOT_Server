from flask import Flask, request, json
from flask_restful import Resource, Api, fields, marshal_with
from flask_httpauth import HTTPBasicAuth
from mongodb_helper import MongodbHelper
from utils import api_response

import datetime

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

USER_DATA = {
    "admin": "SuperSecretPwd"
}

@auth.verify_password
def verify(username:str, password:str):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

class Sensors(Resource):
    def __init__(self):
        self.collection_name = "sensors"
        self.db_dsn = "mongodb://db:27017/"
        self.db_name = "iot"
    @auth.login_required
    def get(self):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        response = list(mongoHelper.list({}))
        return api_response(200, response)

    @auth.login_required
    def post(self):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        json_data = request.get_json(force=True)
        json_data['last_connection_datetime'] = datetime.datetime.now()
        result = mongoHelper.add(json_data)
        return api_response(201, {"object_id":result})

class SensorById(Resource):
    def __init__(self):
        self.collection_name = "sensors"
        self.db_dsn = "mongodb://db:27017/"
        self.db_name = "iot"

    @auth.login_required
    def get(self, object_id):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        response = list(mongoHelper.fetch_by({'_id':object_id}))
        return api_response(200, response)

class Payloads(Resource):
    def __init__(self):
        self.collection_name = "payloads"
        self.db_dsn = "mongodb://db:27017/"
        self.db_name = "iot"
    @auth.login_required
    def post(self):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        json_data = request.get_json(force=True)
        json_data['last_connection_datetime'] = datetime.datetime.now()
        result = mongoHelper.add(json_data)
        return api_response(201, {"object_id":result})

    @auth.login_required
    def get(self):
        # hepsini çekmeyeceksin id ye göre çekeceksin çözmeye çalış
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        response = list(mongoHelper.list({}))
        return api_response(200, response)

class HelloWorld(Resource):
    @auth.login_required
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(Sensors, '/sensors')
api.add_resource(SensorById, '/sensors/<string:object_id>')
api.add_resource(Payloads, '/payloads')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)