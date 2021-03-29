from flask import Flask, jsonify, json, request
from fetch_uv_data import fetch_uv_data
from dbase import insert_uv_index, select_data, insert_data

app = Flask(__name__)

@app.route("/")
def hello():
    html = "<h1>Hello from {name}!</h1>\nGoto /api to fetch UV data".format(name="Mehwish") 
    return html

@app.route("/api", methods=['GET'])
def get_uv_data():
    uv = fetch_uv_data()
    print(uv['result']['uv'], uv['result']['uv_max'], uv['result']['uv_max_time'], uv['result']['uv_time'])
    insert_uv_index(uv['result']['uv'], uv['result']['uv_max'], uv['result']['uv_max_time'], uv['result']['uv_time'])
    return jsonify(uv)


@app.route("/location/<city>/", methods=['GET'])
def get_data(city):
    lat, lng = select_data(city)
    # print(str(city) + ", " + str(lat) + ", " + str(lng))
    try:
        uv = fetch_uv_data(lat, lng)
        return uv, 200
    except:
        return 404



@app.route('/add', methods=['POST'])
def create_a_record():
    if not request.json or not 'city' in request.json:
        return jsonify({'error':'the city record needs to have a lat & long'}), 400
    new_record = {
        'city': request.json['city'],
        'lat' : request.json.get('lat', ''),
        'lng' : request.json.get('lng', ''),
    }
    insert_data(new_record['city'], new_record['lat'], new_record['lng'])
    return jsonify({'message':'new city created: /add/{} and lat:{}, lng:{}'.format(new_record['city'], new_record['lat'], new_record['lng'])}), 201
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
