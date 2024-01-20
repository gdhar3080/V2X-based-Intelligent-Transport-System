# V2X Communication (A reasonably detailed and thoroughly designed network architecture)
(This definitely can be improved on and made better to scale)

This is a network-ish design for data handling and usage after it is obtained from the vehicle.

## How to run:

### 1. Assuming you have a module sending data to an MQTT broker: (from the root folder) - Else jump to step 2.
```
cd backend 
python3 mqtt.py
```
The above commands will initialize the MQTT RECEIVER script. Adjust the topic name and the broker address and port number to suit your needs

### 2. Running the main local server (assuming you're in the backend folder)
```
python3 app.py
```
This will start the server. The server can receive data from the MQTT script and store it in a local database. If the MQTT script is inactive, you can use this to access past stored data (There is a little placeholder data as of now)

### 2.1 Local database (initialising your own)
```
python3
from app import app, fdb
app.app_context().push()
fdb.create_all()
```

The above commands can be executed if you want to create a fresh file for your local database (erase all the placeholder data) - (To erase placeholder data, just delete the backend/instance folder)

### 3. Dashboard UI (from the root directory)
```
cd frontend
npm install 
npm start
```
The above will install all necessary dependencies and also start the dashboard UI. You can monitor your database and also render current location to a map.

On the map, you can also navigate to past positions of your vehicle using the navigation buttons.

The map has live location updation and also shows alerts for hotspots (junctions and probable accident zones) - not very extensive, just a few example spots as of now and also alerts for speeding.

### 4. Mobile application (from root directory)
```
cd mobile
expo install
npx expo start
```

This starts the application on a server which you can access by downloading the 'expo go' app on android and scanning the QR code (no release build as of now sorry)

Contains authentication using firebase auth. Further ensures security by requiring vehicle number to access data from the firebase 'Realtime Database'. Also consists of a map to show the current (last updated) location of the vehicle.
