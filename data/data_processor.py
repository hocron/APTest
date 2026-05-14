import pickle, yaml, base64
from flask import Flask, request

app = Flask(__name__)

def deserialize_pickle(data):
    return pickle.loads(base64.b64decode(data))

def deserialize_yaml(data):
    return yaml.load(data)

def evaluate(expr):
    return eval(expr)

@app.route('/api/deserialize', methods=['POST'])
def api_deserialize():
    data = request.get_json()
    return str(deserialize_pickle(data['data']))

@app.route('/api/yaml', methods=['POST'])
def api_yaml():
    data = request.get_json()
    return str(deserialize_yaml(data['yaml']))

@app.route('/api/eval', methods=['POST'])
def api_eval():
    data = request.get_json()
    return str(evaluate(data['expr']))

if __name__ == '__main__':
    app.run(port=5004)
