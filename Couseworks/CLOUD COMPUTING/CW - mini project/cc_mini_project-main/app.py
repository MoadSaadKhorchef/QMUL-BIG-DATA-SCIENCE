from flask import Flask, render_template, redirect, url_for, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()


users = {
    "username": generate_password_hash("password"),
}

users1 = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get("username"), password):
        return username


@app.route("/")
@auth.login_required
def index():
    return f"You have successfully logged in, {auth.current_user()}"
   
    
if __name__ == "__main__":
    app.run()