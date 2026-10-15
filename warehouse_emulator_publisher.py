import paho.mqtt.client as mqtt
import random as rnd
import json as js
import time

def data_generator(id):
    current_temperature = rnd.uniform(20, 30)  # Simulated temperature value        
    anomaly = rnd.uniform(0,20)
    is_anomaly = False
    json_dumped = {}
    if anomaly > 13:
        current_temperature = -5  # Simulate an anomaly by adding a random value between 5 and 10
        is_anomaly = True
        json_dumped = {
            "device_id": id,
            "temperature": -5,
            "humidity": 45.2,
            "unit": "C",
            "ts": "2026-10-15T20:00:00Z",
            "alert": True
            }
    else:
        json_dumped = {
                "device_id": id,
                "temperature": 22.5,
                "humidity": 45.2,
                "unit": "C",
                "ts": "2026-10-15T20:00:00Z",
                }
    return js.dumps(json_dumped)

client = mqtt.Client()
try:
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_start()
    while True:
        for i in range(5):
          a = ["A", "B", "C", "D", "E"]
          data_sensor = data_generator("Zone" + a[i])       
          topic = f"warehouse/zone-{a[i]}/temperature"
          client.publish(topic, data_sensor, qos=1)
          print(topic + "\n")
        time.sleep(1.5)
except Exception as e:
    print(f"Exception with Error: {e}")
except KeyboardInterrupt:
    print(f"Keyboard interrupt exception")
finally:
    client.loop_stop()
    client.disconnect()