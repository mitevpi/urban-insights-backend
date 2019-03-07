import json
import os

from flask import Flask
from flask import request
from flask.json import jsonify
from flask_cors import CORS

from address_to_sun_vector import getSunVector
from obj import cutObj

app = Flask(__name__)

resource_path = os.path.join(app.root_path, 'models')
CORS(app)

@app.route("/")
def home():
    return jsonify({'test': 1})

@app.route("/testRequest", methods=['POST'])
def testRequest():
    try:
        data = json.loads(request.data)
    except:
        data = "empty"

    try:
        args = json.loads(request.args)
    except:
        args = "empty"

    try:
        values = json.loads(request.values)
    except:
        values = "empty"

    try:
        reqJson = request.json
    except:
        reqJson = "empty"

    return jsonify({'data':data, 'args': args, 'values': values, 'reqJson': reqJson})

@app.route("/getSunVector", methods=['POST', 'GET'])
def runSunVector():
    data = json.loads(request.data)
    vector = getSunVector(data['address'], data['month'], data['day'], data['hour'])

    return jsonify({'sunVector': vector, 'request': data})


@app.route("/getCutObj")
def runCutObj():
    flines = cutObj()
    return jsonify({'parsedModel': flines})


if __name__ == "__main":
    app.run()
