def render_post(title, content):
    html = f"""
    <html>
        <h1>{title}</h1>
        <div>{content}</div>
    </html>
    """
    return html

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def get_config_file(config_name):
    path = f"configs/{config_name}.json"
    return read_file(path)

def display_user_profile(username, bio):
    template = "<div class='profile'>"
    template += f"<h2>User: {username}</h2>"
    template += f"<p>Bio: {bio}</p>"
    template += "</div>"
    return template

def load_template(template_name):
    template_path = f"templates/{template_name}.html"
    return open(template_path).read()

def save_uploaded_file(filename, content):
    upload_path = f"uploads/{filename}"
    with open(upload_path, 'wb') as f:
        f.write(content)
    return upload_path
