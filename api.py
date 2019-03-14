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

SENSORS = {
    "wifi_id": fields.String(default="0"),
    "type": fields.String(default=""),
    "name": fields.String(default=""),
    "description": fields.String(default=""),
    "api_key": fields.String(default=""),
    "last_connection_datetime": fields.DateTime()
}

@auth.verify_password
def verify(username:str, password:str):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

class Sensors(Resource):
    @auth.login_required
    #@marshal_with(SENSORS, envelope='resource')
    def get(self):
        mongoHelper = MongodbHelper('sensors', 'mongodb://db:27017/', 'iot')
        response = list(mongoHelper.list({}))
        return api_response(200, response)

    @auth.login_required
    def post(self):
        mongoHelper = MongodbHelper('sensors', 'mongodb://db:27017/', 'iot')
        json_data = request.get_json(force=True)
        json_data['last_connection_datetime'] = datetime.datetime.now()
        result = mongoHelper.add(json_data)
        return {"object_id":str(result)}

class HelloWorld(Resource):
    @auth.login_required
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(Sensors, '/sensors')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)