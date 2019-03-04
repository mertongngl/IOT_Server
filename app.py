#!flask/bin/python
from flask import Flask
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

@app.route('/get')
def getAllFuckinItems():
    mongoHelper = MongodbHelper('data','mongodb://db:27017/','iot')
    all_results = mongoHelper.get_all({})
    return str(all_results)

if __name__ == '__main__':
    app.run()