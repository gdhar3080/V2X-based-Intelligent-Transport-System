import paho.mqtt.client as mqtt
import requests
import json

mqtt_broker_address = "Gauravs-MacBook-Air.local"  
mqtt_broker_port = 1883 

def on_message(client, userdata, msg):
    data = msg.payload.decode('utf-8')
    # print(f"Data received from NodeMCU: {data}")
    data_parsed = json.loads(data)
    
    server_url = 'http://127.0.0.1:5000'
    index_route_url = f'{server_url}/vehicle'

    try:
        response = requests.post(index_route_url, json=data_parsed)

        if response.status_code == 200:
            print(f"Data successfully posted to the index route: {response}")
        else:
            print(f"Failed to post data to the index route. Status code: {response.status_code}")
    except:
        print("Something seriously went wrong")

mqtt_client = mqtt.Client("python_script_subscriber1")
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker_address, mqtt_broker_port, 60)
mqtt_client.subscribe("/nodemcu/car1")  

mqtt_client.loop_forever()
