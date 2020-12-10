from main import app
from flask import request, jsonify
from database_queries import loginQueries, tokenQueries

import json

@app.route('/client/create', methods=['POST'])
def createClient():
    if request.method == 'POST':
        data = json.loads(request.data)
        if loginQueries.createClient(data["uid"]) is True:
            return jsonify('User created'), 200
        else:
            return jsonify('Database error'), 200
    else:
        return 405

@app.route('/client/<uid>/login', methods=['GET'])
def loginClient(uid = None):
    if request.method == 'GET':
        if tokenQueries.generateTokens(uid) is True:
            return jsonify('Tokens assigned'), 200
        else:
            return jsonify('Database error'), 200
    else:
        return 405

@app.route('/client/<uid>/info', methods=['GET'])
def getClient(uid = None):
    if request.method == 'GET':
        result = loginQueries.getClient(uid)
        if result is not False:
            return jsonify(result), 200
        else:
            return jsonify('FAILURE'), 200
    else:
        return 405

@app.route('/client/<uid>/logout', methods=['POST'])
def logoutClient(uid = None):
    if request.method == 'POST':
        return jsonify('OK'), 200

@app.route('/client/<uid>/update', methods=['PUT'])
def updateClient(uid = None):
    if request.method == 'PUT':
        data = json.loads(request.data)
        if loginQueries.updateClient(data, uid) is True:
            return jsonify('OK'), 200
        else:
            return jsonify('FAILURE'), 200
    else:
        return 405

