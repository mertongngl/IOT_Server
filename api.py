from flask import Flask, request, json
from flask_restful import Resource, Api, fields, marshal_with
from flask_httpauth import HTTPBasicAuth
from mongodb_helper import MongodbHelper
from bson import ObjectId
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

    @auth.login_required
    def delete(self):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        deleted_count = mongoHelper.remove_all()    
        if deleted_count == 0:
            return api_response(400, "Cannot delete all sensors")

        return api_response(200, "Delete all payloads succesfully")

class SensorById(Resource):
    def __init__(self):
        self.collection_name = "sensors"
        self.db_dsn = "mongodb://db:27017/"
        self.db_name = "iot"

    @auth.login_required
    def get(self, object_id):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        query_object = {'_id': ObjectId(object_id)}
        response = list(mongoHelper.list(query_object))

        if not response:
            return api_response(404, "Sensor not found which has '{}' object_id".format(object_id))

        return api_response(200, response)

    @auth.login_required
    def delete(self, object_id):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        query_object = {'_id': ObjectId(object_id)}
        deleted_count = mongoHelper.remove(query_object)

        if deleted_count == 0:
            return api_response(400, "Cannot delete sensor because there is no sensor which has '{}' object_id".format(object_id))

        return api_response(200, "Delete sensor succesfully which has '{}' object_id".format(object_id))

    @auth.login_required
    def put(self, object_id):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        query_object = {'_id': ObjectId(object_id)}
        json_data = request.get_json(force=True)
        json_data['last_connection_datetime'] = datetime.datetime.now()
        response = {"modified_count": mongoHelper.edit(query_object, json_data)}

        if response == 0:
            return api_response(400, "Cannot be edit")

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
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        response = list(mongoHelper.list({}))
        return api_response(200, response)

    @auth.login_required
    def delete(self):
        mongoHelper = MongodbHelper(self.collection_name, self.db_dsn, self.db_name)
        deleted_count = mongoHelper.remove_all()    
        if deleted_count == 0:
            return api_response(400, "Cannot delete all payloads")

        return api_response(200, "Delete all payloads succesfully")


class HelloWorld(Resource):
    @auth.login_required
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(Sensors, '/sensors')
api.add_resource(SensorById, '/sensor/<string:object_id>')
api.add_resource(Payloads, '/payloads')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)