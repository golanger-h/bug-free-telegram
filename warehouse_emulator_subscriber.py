import paho.mqtt.client as mqtt
import json
import threading
import time
import datetime as dt

import parser as dg
import stats as st
import logs as log

stats = {
    "total": 0,
    "alerts": 0,
    "avg": {}
}
logger = open("logs/warehouse.log", "a", buffering=1)
alerter = open("logs/alerts.log", "a", buffering=1)

threading.Timer(10.0, st.print_stat, args=(stats,)).start()

def on_connect(client, userdata, flags, rc, properties=None):
    print("client connected with code: " + str(rc))
    client.subscribe("warehouse/+/temperature", qos=1)
    print("subscribed to topic: warehouse/+/temperature")

def on_message(client, userdata, msg):
    stats["total"] += 1

    try:
        info = dg.pars_json_from_decoded_payload(msg.payload.decode())

        st.generate_stat(info, stats)
        logger.write(log.generate_log(info))
        if  "alerts" in info:
            alerter.write(log.generate_alert(info))
        
    except Exception as e:
        print(f"exception: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("broker.emqx.io", 1883, 60)
    time.sleep(1)
    client.loop_forever()
except Exception as e:
    print(f"Exception: {e}")
except KeyboardInterrupt:
    print("keyboard interrupt")
finally:
    logger.close()
    alerter.close()
    client.disconnect()



