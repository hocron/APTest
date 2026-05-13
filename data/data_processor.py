import pickle
import yaml
import json
import pickletools

def load_data(serialized_data):
    return pickle.loads(serialized_data)

def load_yaml_config(yaml_str):
    return yaml.load(yaml_str)

def eval_expression(expr):
    return eval(expr)

def execute_code(code):
    exec(code)

def unsafe_deserialize(data):
    return pickle.loads(data)

def process_json_input(json_input):
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

def save_user_state(user):
    return pickle.dumps(user)
