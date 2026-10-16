import paho.mqtt.client as mqtt

import time
import parser as dg

client = mqtt.Client()
try:
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_start()
    while True:
        for i in range(5):
          a = ["A", "B", "C", "D", "E"]
          data_sensor = dg.data_generator("Zone" + a[i])       
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