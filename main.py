#!flask/bin/python
from flask import Flask, jsonify, request
from client import Client
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://172.18.0.35:27017/DBstocker"

mongo = PyMongo(app)

#listClient = [
#    Client(0,'Paulo','123','email@gmail.com'),
#    Client(1,'Pablo','456','email@hotmail.com'),
#    Client(2,'Pedro','789','email@zipmail.com')
#]

@app.route('/api/v1.0/clients', methods=['GET'])
def get_clients():
    clients = []
    for c in mongo.db.clients.find() :
        newClient = Client()
        newClient._id = str(c['_id'])
        newClient.name = c['name']
        newClient.phone = c['phone']
        newClient.email = c['email']
        clients.append(newClient)

    return jsonify([cli.__dict__ for cli in clients]), 200

@app.route('/api/v1.0/clients', methods=['POST'])
def post_clients():
    newClient = Client()
    newClient._id = ObjectId()
    newClient.name = request.json['name']
    newClient.phone = request.json['phone']
    newClient.email = request.json['email']

    ret = mongo.db.clients.insert_one(newClient.__dict__).inserted_id
    return jsonify({'id': str(ret)}), 201

@app.route('/api/v1.0/clients/<string:_id>', methods=['PUT'])
def put_clients(_id):
    updClient = Client()
    updClient._id = ObjectId(_id)
    updClient.name = request.json['name']
    updClient.phone = request.json['phone']
    updClient.email = request.json['email']

    ret = mongo.db.clients.update_one({'_id':updClient._id},{'$set':updClient.__dict__}, upsert=False)

    if int(ret.matched_count) > 0 & int(ret.modified_count) > 0:
        return jsonify({'id': _id,'updated': True}), 200
    elif int(ret.matched_count) == 0 :
        return jsonify({'id': _id,'updated': False,'message':'Not found'}), 200
    else :
        return jsonify({'id': _id,'updated': False,'message':'Cannot update'}), 200


@app.route('/api/v1.0/clients/<string:_id>', methods=['DELETE'])
def delete_clients(_id):
    updClient = Client()
    updClient._id = ObjectId(_id)

    ret = mongo.db.clients.delete_one({'_id':updClient._id}).deleted_count
    if int(ret) > 0 :
        return jsonify({'id': _id,'deleted': True, 'deleted_count': str(ret)}), 200
    else :
        return jsonify({'id': _id,'deleted': False}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
