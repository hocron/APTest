from flask import Flask, request

app = Flask(__name__)

def render_post(title, content):
    return f"<html><h1>{title}</h1><div>{content}</div></html>"

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

@app.route('/api/render')
def api_render():
    return render_post(request.args.get('title'), request.args.get('content'))

@app.route('/api/read')
def api_read():
    return read_file(request.args.get('filename'))

if __name__ == '__main__':
    app.run(port=5003)
