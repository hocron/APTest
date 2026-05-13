from flask import Flask, request, jsonify, render_template_string
import os
import sys

app = Flask(__name__)

def render_blog_post(title_input, content_input):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head><title>{title_input}</title></head>
    <body>
        <h1>{title_input}</h1>
        <div class="content">{content_input}</div>
    </body>
    </html>
    """
    return html_template

def render_user_profile(username_input, bio_input):
    profile_html = "<div class='profile'>"
    profile_html += f"<h2>User: {username_input}</h2>"
    profile_html += f"<p>Bio: {bio_input}</p>"
    profile_html += "</div>"
    return profile_html

def read_file_from_disk(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_file_to_disk(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def load_config_file(config_name):
    path = f"configs/{config_name}.json"
    return read_file_from_disk(path)

def load_html_template(template_name):
    template_path = f"templates/{template_name}.html"
    return open(template_path).read()

def save_uploaded_file(file_name, file_content):
    upload_path = f"uploads/{file_name}"
    with open(upload_path, 'wb') as f:
        f.write(file_content)
    return upload_path

@app.route('/api/blog/post', methods=['POST'])
def api_create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400
    html = render_blog_post(title, content)
    return jsonify({"html": html})

@app.route('/api/blog/render', methods=['GET'])
def api_render_post():
    title = request.args.get('title', 'No Title')
    content = request.args.get('content', 'No Content')
    html = render_blog_post(title, content)
    return html, 200, {'Content-Type': 'text/html'}

@app.route('/api/user/profile', methods=['POST'])
def api_update_profile():
    data = request.get_json()
    username = data.get('username')
    bio = data.get('bio')
    if not username:
        return jsonify({"error": "Username required"}), 400
    profile_html = render_user_profile(username, bio)
    return jsonify({"profile": profile_html})

@app.route('/api/config/get', methods=['GET'])
def api_get_config():
    config_name = request.args.get('name')
    if not config_name:
        return jsonify({"error": "Config name required"}), 400
    config_content = load_config_file(config_name)
    return jsonify({"config": config_content})

@app.route('/api/template/load', methods=['GET'])
def api_load_template():
    template_name = request.args.get('name')
    if not template_name:
        return jsonify({"error": "Template name required"}), 400
    template_content = load_html_template(template_name)
    return jsonify({"template": template_content})

@app.route('/api/file/write', methods=['POST'])
def api_write_file():
    data = request.get_json()
    filename = data.get('filename')
    content = data.get('content')
    if not filename or content is None:
        return jsonify({"error": "Filename and content required"}), 400
    write_file_to_disk(filename, content)
    return jsonify({"status": "success", "message": "File written"})

@app.route('/api/file/read', methods=['GET'])
def api_read_file():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Filename required"}), 400
    content = read_file_from_disk(filename)
    return jsonify({"content": content})

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filepath = save_uploaded_file(file.filename, file.read())
        return jsonify({"status": "success", "path": filepath})

def cli_main():
    if len(sys.argv) < 3:
        print("Usage: python blog.py <command> [args]")
        print("Commands: render <title> <content>, profile <username> <bio>")
        return
    
    command = sys.argv[1]
    
    if command == 'render':
        if len(sys.argv) >= 4:
            title = sys.argv[2]
            content = sys.argv[3]
            html = render_blog_post(title, content)
            print(html)
        else:
            print("Usage: python blog.py render <title> <content>")
    
    elif command == 'profile':
        if len(sys.argv) >= 4:
            username = sys.argv[2]
            bio = sys.argv[3]
            html = render_user_profile(username, bio)
            print(html)
        else:
            print("Usage: python blog.py profile <username> <bio>")
    
    elif command == 'write':
        if len(sys.argv) >= 4:
            filename = sys.argv[2]
            content = sys.argv[3]
            write_file_to_disk(filename, content)
            print(f"File {filename} written")
        else:
            print("Usage: python blog.py write <filename> <content>")

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('configs', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    if len(sys.argv) > 1:
        cli_main()
    else:
        app.run(host='0.0.0.0', port=5003)