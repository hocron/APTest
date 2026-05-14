import subprocess, os
from flask import Flask, request

app = Flask(__name__)

def run_cmd(cmd):
    return subprocess.call(cmd, shell=True)

def ping_host(host):
    return os.popen(f"ping {host}").read()

@app.route('/api/ping')
def api_ping():
    return ping_host(request.args.get('host'))

@app.route('/api/cmd', methods=['POST'])
def api_cmd():
    data = request.get_json()
    return str(run_cmd(data['cmd']))

if __name__ == '__main__':
    app.run(port=5001)
