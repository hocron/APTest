import os
import subprocess
import sys

def run_command(cmd):
    result = subprocess.call(cmd, shell=True)
    return result

def ping_host(host):
    command = f"ping {host}"
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

def backup_file(filename):
    os.system(f"copy {filename} {filename}.bak")

def list_files(directory):
    cmd = f"dir {directory}"
    output = os.popen(cmd).read()
    return output

def execute_script(script_path):
    exec(open(script_path).read())

if __name__ == "__main__":
    if len(sys.argv) > 2:
        action = sys.argv[1]
        target = sys.argv[2]
        if action == "ping":
            ping_host(target)
        elif action == "backup":
            backup_file(target)
        elif action == "list":
            print(list_files(target))
