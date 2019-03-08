#!flask/bin/python
from flask import Flask,jsonify,request
from mongodb_helper import MongodbHelper

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/test')
def test():
    mongoHelper = MongodbHelper('data','mongodb://db:27017/','iot')
    inserted_id = mongoHelper.add({"name":"mert","surname":"ongengil"})
    return str(inserted_id)

@app.route('/auth')
def auth():
    pass

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    mongoHelper = MongodbHelper('users', 'mongodb://db:27017/', 'iot')
    inserted_id = mongoHelper.add({"username":username,"password":password,"is_active": True})

    return '''
        <h1> 
        Registration was successfull!
        Object ID: {}
        </h1>
    '''.format(inserted_id)


if __name__ == '__main__':
    app.run()