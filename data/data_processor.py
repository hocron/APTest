import pickle
import yaml
import json
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

def deserialize_pickle(data):
    return pickle.loads(data)

def deserialize_yaml(yaml_str):
    return yaml.load(yaml_str)

def evaluate_expression(expr):
    return eval(expr)

def execute_dynamic_code(code):
    exec(code)

def process_json_with_command(json_input):
    data = json.loads(json_input)
    if 'command' in data:
        eval(data['command'])
    return data

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def __reduce__(self):
        return (eval, ("__import__('os').system('whoami')",))

def serialize_user(user):
    return pickle.dumps(user)

def load_user_from_pickle(pickle_data):
    return pickle.loads(pickle_data)

@app.route('/api/data/deserialize', methods=['POST'])
def api_deserialize():
    data = request.get_json()
    serialized = data.get('data')
    format_type = data.get('format', 'pickle')
    
    if not serialized:
        return jsonify({"error": "Data required"}), 400
    
    try:
        if format_type == 'pickle':
            decoded = base64.b64decode(serialized)
            result = deserialize_pickle(decoded)
        elif format_type == 'yaml':
            result = deserialize_yaml(serialized)
        else:
            return jsonify({"error": "Unsupported format"}), 400
        
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/eval', methods=['POST'])
def api_eval():
    data = request.get_json()
    expression = data.get('expression')
    
    if not expression:
        return jsonify({"error": "Expression required"}), 400
    
    try:
        result = evaluate_expression(expression)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/exec', methods=['POST'])
def api_exec():
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return jsonify({"error": "Code required"}), 400
    
    try:
        execute_dynamic_code(code)
        return jsonify({"status": "success", "message": "Code executed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/json', methods=['POST'])
def api_process_json():
    json_input = request.get_json()
    if not json_input:
        return jsonify({"error": "JSON input required"}), 400
    
    try:
        json_str = json.dumps(json_input)
        result = process_json_with_command(json_str)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/user/save', methods=['POST'])
def api_save_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400
    
    user = User(name, email)
    serialized = serialize_user(user)
    encoded = base64.b64encode(serialized).decode()
    
    return jsonify({"serialized_user": encoded})

@app.route('/api/data/user/load', methods=['POST'])
def api_load_user():
    data = request.get_json()
    serialized = data.get('serialized_user')
    
    if not serialized:
        return jsonify({"error": "Serialized user data required"}), 400
    
    try:
        decoded = base64.b64decode(serialized)
        user = load_user_from_pickle(decoded)
        return jsonify({"user": {"name": user.name, "email": user.email}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def cli_main():
    if len(sys.argv) < 3:
        print("Usage: python data_processor.py <command> <data>")
        print("Commands: eval, exec, deserialize")
        return
    
    command = sys.argv[1]
    input_data = sys.argv[2]
    
    if command == 'eval':
        result = evaluate_expression(input_data)
        print(f"Result: {result}")
    
    elif command == 'exec':
        execute_dynamic_code(input_data)
        print("Code executed")
    
    elif command == 'deserialize':
        try:
            decoded = base64.b64decode(input_data)
            result = deserialize_pickle(decoded)
            print(f"Deserialized: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import base64
    if len(sys.argv) > 1:
        cli_main()
    else:
        app.run(host='0.0.0.0', port=5004)