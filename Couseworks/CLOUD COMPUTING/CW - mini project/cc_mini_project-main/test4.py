from flask import Flask
from flask import jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

@app.route('/rest-auth')
@auth.login_required
def get_response():
	return jsonify('You are authorized to see this message')
    
@auth.verify_password
def authenticate(username, password):
    if username and password:
        if username == 'moe' and password == 'moe':
             return True
        else:
            return False
    return False

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401
		
if __name__ == "__main__":
    app.run()