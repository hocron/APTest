import os
import subprocess
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

def execute_system_command(cmd):
    result = subprocess.call(cmd, shell=True)
    return result

def ping_target_host(host):
    command = f"ping {host}"
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def backup_system_file(filename):
    os.system(f"copy {filename} {filename}.bak")

def list_directory_contents(directory):
    cmd = f"dir {directory}"
    output = os.popen(cmd).read()
    return output

def load_and_execute_script(script_path):
    exec(open(script_path).read())

@app.route('/api/system/ping', methods=['GET'])
def api_ping_host():
    host = request.args.get('host')
    if not host:
        return jsonify({"error": "Host parameter required"}), 400
    process = ping_target_host(host)
    stdout, stderr = process.communicate()
    return jsonify({"output": stdout.decode('gbk', errors='ignore'), "error": stderr.decode('gbk', errors='ignore')})

@app.route('/api/system/backup', methods=['POST'])
def api_backup_file():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({"error": "Filename parameter required"}), 400
    backup_system_file(filename)
    return jsonify({"status": "success", "message": "Backup completed"})

@app.route('/api/system/list', methods=['GET'])
def api_list_directory():
    directory = request.args.get('dir', '.')
    contents = list_directory_contents(directory)
    return jsonify({"directory": directory, "contents": contents})

@app.route('/api/system/execute', methods=['POST'])
def api_execute_command():
    data = request.get_json()
    command = data.get('command')
    if not command:
        return jsonify({"error": "Command parameter required"}), 400
    result = execute_system_command(command)
    return jsonify({"status": "completed", "exit_code": result})

@app.route('/api/system/script', methods=['POST'])
def api_run_script():
    data = request.get_json()
    script_path = data.get('script_path')
    if not script_path:
        return jsonify({"error": "Script path required"}), 400
    load_and_execute_script(script_path)
    return jsonify({"status": "success", "message": "Script executed"})

def cli_main():
    if len(sys.argv) < 3:
        print("Usage: python system_admin.py <command> <target>")
        print("Commands: ping, backup, list, execute")
        return
    
    command = sys.argv[1]
    target = sys.argv[2]
    
    if command == 'ping':
        process = ping_target_host(target)
        stdout, stderr = process.communicate()
        print(stdout.decode('gbk', errors='ignore'))
    
    elif command == 'backup':
        backup_system_file(target)
        print(f"Backup of {target} completed")
    
    elif command == 'list':
        contents = list_directory_contents(target)
        print(contents)
    
    elif command == 'execute':
        result = execute_system_command(target)
        print(f"Command executed with exit code: {result}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_main()
    else:
        app.run(host='0.0.0.0', port=5001)