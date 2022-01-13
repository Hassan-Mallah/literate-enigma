from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import environ  # for .env
from utils import *

env = environ.Env()
# reading .env file
environ.Env.read_env()

app = Flask(__name__)

username = env('username')
password = env('password')

# app config
app.config['MONGO_URI'] = 'mongodb+srv://{}:{}@cluster0.rthfj.mongodb.net/test?retryWrites=true&w=majority'.format(
    username, password)
app.config['MONGO_DBNAME'] = 'test'

# connect to mongo db
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def index():
    return 'Hello to pymongo flask api :)'


@app.route('/framework', methods=['GET'])
def get_all_frameworks():
    # framework is collection name
    framework = mongo.db.framework

    # get records and save them to a list of dicts
    output = []
    for q in framework.find():
        output.append({'name': q['name'], 'language': q['language']})

    return jsonify({'result': output})


@app.route('/framework/<name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.db.framework

    q = framework.find_one({'name': name})
    if q:
        output = {
            'name': q['name'],
            'language': q['language']
        }
    else:
        output = 'Not found'

    return jsonify({'result': output})


@app.route('/framework', methods=['POST'])
def add_framework():
    # e.g.  curl -X POST http://127.0.0.1:5000/framework -d '{"name":"value1", "language":"value2"}'  -H "Content-Type: application/json"

    framework = mongo.db.framework

    # get data from request
    name = request.json['name']
    language = request.json['language']

    # insert one and save result
    framework_id = framework.insert_one({'name': name, 'language': language})

    # get record by id
    new_framework = framework.find_one({'_id': framework_id.inserted_id})

    # return inserted record
    output = {'name': new_framework['name'], 'language': new_framework['language']}

    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
