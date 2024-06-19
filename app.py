import os
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SECRET_KEY'] = '57iz5UrMmNgKMxRKYVSkrcuGV61ACTAhGxM9qgJ8xBU='  # Change this to a secure random key in production
jwt = JWTManager(app)

# Static user (for demonstration)
users = {
    'john_doe': 'password123'  # Replace with a secure password hash in production
}

# Endpoint that requires authentication
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return f'Hello, {current_user}, you are authenticated!'

# Your existing endpoints
@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    if name:
        print(f'Request for hello page received with name={name}')
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

# Endpoint to generate JWT token for authentication (for demo purposes)
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    else:
        return {'error': 'Invalid username or password'}, 401

if __name__ == '__main__':
    app.run(debug=True)
