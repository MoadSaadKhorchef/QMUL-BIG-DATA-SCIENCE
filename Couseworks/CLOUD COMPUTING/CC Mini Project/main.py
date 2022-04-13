from flask import Flask, jsonify, request
from fetch_uv_data import fetch_uv_data, retrieve_data
from dbase import select_data, insert_data, delete_record, modify_record, insert_user, select_user
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()
role = ''

# GET
@app.route("/location/<city>/", methods=['GET'])
@auth.login_required
def get_data(city):
    try:
        lat, lng = select_data(city)
        ext_api_data = retrieve_data(lat, lng)
        return jsonify(ext_api_data), 200
    except:
        return jsonify({'error':'city not found'}), 404


# POST
@app.route('/add', methods=['POST'])
@auth.login_required(role='admin')
def create_a_record():
    if not request.json or not all(k in request.json for k in ['city', 'lat', 'lng']):
        return jsonify({'error':'the city record needs to have a city, lat & long'}), 400
    new_record = {
        'city': request.json['city'],
        'lat' : request.json.get('lat', ''),
        'lng' : request.json.get('lng', ''),
    }
    insert_data(new_record['city'], new_record['lat'], new_record['lng'])
    return jsonify({'message':'new city created: /add/{} and lat:{}, lng:{}'.format(new_record['city'], new_record['lat'], new_record['lng'])}), 201


# PUT
@app.route('/edit', methods=['PUT'])
@auth.login_required(role='admin')
def edit_record():
    if not request.json or not all(k in request.json for k in ['city', 'lat', 'lng']):
        return jsonify({'error':'the city record needs to have a city, lat & long'}), 400
    new_record = {
        'city': request.json['city'],
        'lat' : request.json.get('lat', ''),
        'lng' : request.json.get('lng', ''),
    }
    
    status = modify_record(new_record['city'], new_record['lat'], new_record['lng'])
    
    return jsonify({'success': status}), 201


# DELETE
@app.route('/delete/<city>', methods=['DELETE'])
@auth.login_required(role='admin')
def delete_a_record(city): 
    
    status = delete_record(city)
    if status:
        return jsonify({'success': f'Deleted {city}'}), 200
    else:    
        return jsonify({'error': 'Record not found'}), 404     

# POST
@app.route('/add_user', methods=['POST'])
@auth.login_required(role='admin')
def create_a_user():
    if not request.json or not all(k in request.json for k in ['userName', 'password', 'role']):
        return jsonify({'error':'the new user needs to have user name, password, and role'}), 400
    new_record = {
        'userName': request.json.get('userName', ''),
        'password' : request.json.get('password', ''),
        'role' : request.json.get('role', ''),
    }
    insert_user(new_record['userName'], generate_password_hash(new_record['password']), new_record['role'])
    return jsonify({'message':'new user created'}), 201
       
        
@auth.verify_password
def authenticate(username, password):
    role = 0
    if username and password:       
        account = select_user(username)  
        if account and check_password_hash(account[1], password):
            role = account[2]
            return role
        else:
            return False
    return False


@auth.get_user_roles
def get_user_roles(role):       
    return role
    
    
@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401
      

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
