from flask import Flask, request, jsonify
from rtree import index
import mysql.connector

app = Flask(__name__)

idx = index.Index()

connection = mysql.connector.connect(
    host="172.17.0.2",
    user="root",
    password="my-secret-pw",
    database="bicycle_data"
)

cursor = connection.cursor()

cursor.execute("SELECT latitude, longitude, bicycle_id FROM bicycle_location")
bicycle_data = cursor.fetchall()

for i, (latitude, longitude, _) in enumerate(bicycle_data):
    idx.insert(i, (latitude, longitude))

@app.route('/closest_bicycle', methods=['GET'])
def closest_bicycle():
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
    except ValueError:
        return jsonify({'error': 'Invalid latitude or longitude provided'}), 400

    closest_idx = list(idx.nearest((latitude, longitude), 1))[0]
    closest_bicycle = bicycle_data[closest_idx]

    response = {
        'bicycle_id': closest_bicycle[2],
        'latitude': closest_bicycle[0],
        'longitude': closest_bicycle[1]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
