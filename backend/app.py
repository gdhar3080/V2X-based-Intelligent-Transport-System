from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from firebase_admin import credentials, db
import firebase_admin
import copy
import json
import time

user_email1 = 'scorchedeyeball@gmail,com'
user_email2 = 'manishanand248@gmail,com'
cred = credentials.Certificate("/Users/gaurav/Desktop/PleaseWork/backend/credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://v2x-app-default-rtdb.asia-southeast1.firebasedatabase.app/"})

ref = db.reference('/')
users_ref = ref.child('vehicle')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdata.db'
fdb = SQLAlchemy(app)
hotspots_file_path = 'hotspots.txt'

mqtt_broker_address = "Gauravs-MacBook-Air.local"  
mqtt_broker_port = 1883 

def read_hotspots_from_file(file_path):
    data = open(file_path, "r").read()
    hotspots = json.loads(data)
    return hotspots

def check_coordinates(input_lon, input_lat, hotspot):
    lower_limit_lon = float(hotspot["lower_limit_lon"])
    upper_limit_lon = float(hotspot["upper_limit_lon"])
    lower_limit_lat = float(hotspot["lower_limit_lat"])
    upper_limit_lat = float(hotspot["upper_limit_lat"])

    if lower_limit_lon <= input_lon <= upper_limit_lon and lower_limit_lat <= input_lat <= upper_limit_lat:
        return True
    else:
        return False

def check_hotspots(input_lon, input_lat, hotspots):
    for hotspot_value in hotspots.values():
        if check_coordinates(input_lat, input_lon, hotspot_value):
            return True
    return False
        
hotspots = read_hotspots_from_file(hotspots_file_path)

def time_finder():
    current = datetime.now()
    return current.strftime('%Y-%m-%d %H:%M:%S')

class Vehicle(fdb.Model):
    id = fdb.Column(fdb.Integer, primary_key=True)
    car_number = fdb.Column(fdb.String(30), nullable=False)
    latitude = fdb.Column(fdb.Float, default=0)
    longitude = fdb.Column(fdb.Float, default=0)
    altitude = fdb.Column(fdb.Float, default=0)
    speed = fdb.Column(fdb.Integer, default=0)
    brake_status = fdb.Column(fdb.String(10), default="Low")
    timestamp = fdb.Column(fdb.String(30), default=time_finder)
    hotspot = fdb.Column(fdb.Boolean, default=False)

@app.route('/vehicle', methods=['POST', 'GET'])
def index():
    # print(request.method)
    vehicle_data = Vehicle.query.order_by(Vehicle.id.desc()).all()
    json_string = [vehicle.__dict__ for vehicle in vehicle_data]
    for item in json_string:
        del item['_sa_instance_state']
    output_json = json.dumps(json_string)

    if request.method == 'POST':
        received = request.data.decode('utf-8')
        final = json.loads(received)
        app_data = Vehicle(**final)
        app_data.id = int(time.time())
        app_data.hotspot = check_hotspots(app_data.latitude, app_data.longitude, hotspots)
        modified_data = copy.deepcopy(app_data)
        modified_data = modified_data.__dict__
        del modified_data['_sa_instance_state']
        if modified_data['car_number'] == 'AX63TY8123':
            new_ref = users_ref.child(f'{user_email1}/{modified_data['car_number']}/{modified_data['id']}')
        elif modified_data['car_number'] == 'XY12AB3456':
            new_ref = users_ref.child(f'{user_email2}/{modified_data['car_number']}/{modified_data['id']}')

        try:
            fdb.session.add(app_data)
            fdb.session.commit()

            del modified_data['id']
            del modified_data['car_number']
            del modified_data['hotspot']
            new_ref.set(modified_data)
            return output_json
    
        except:
            return 'There was an issue adding your info'
        
    else: 
        return output_json

if __name__ == "__main__":
    app.run(debug=True)
