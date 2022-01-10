from flask import Flask, jsonify
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
        output.append({'name': q.name, 'language': q.language})

    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
