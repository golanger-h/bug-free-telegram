import paho.mqtt.client as mqtt
import json
import threading
import time

stats = {
    "total": 0,
    "alerts": 0,
    "avg": {}
}

def print_stat():
    print("-"*3 + "STATS" + "-"*3)
    print(f"Total messages: {stats['total']}")
    print(f"Alerts: {stats['alerts']}")
    print("Avg temp per zone:")
    for zone, temp in stats['avg'].items():
        print(f"  {zone}: {temp['alltmp'] / temp['count']}")
    print("-"*3 + "-----" + "-"*3)
    threading.Timer(10.0, print_stat).start()

threading.Timer(10.0, print_stat).start()

def on_connect(client, userdata, flags, rc, properties=None):
    print("client connected with code: " + str(rc))
    client.subscribe("warehouse/+/temperature", qos=1)
    print("subscribed to topic: warehouse/+/temperature")

def on_message(client, userdata, msg):
    logger = open("warehouse.log", "a", buffering=1)
    alerter = open("alerts.log", "a", buffering=1)

    stats["total"] += 1

    try:
        info = json.loads(msg.payload.decode())
        id = -1
        temp = -1
        ts = info["ts"]
        id = info["device_id"]
        temp = info["temperature"]
        if id in stats["avg"]:
            if "alltmp" in stats["avg"][id]:
                stats["avg"][id]["alltmp"] += temp
            else:
                stats["avg"][id]["alltmp"] = temp
            if "count" in stats["avg"][id]:
                stats["avg"][id]["count"] += 1
            else:
                stats["avg"][id]["count"] = 1
        else:
            stats["avg"][id] = {"alltmp": temp, "count": 1}

        logger.write(f"[{ts}] {id} temp={temp} hum={info['humidity']}\n")
        if  "alerts" in info:
            stats["alerts"] += 1
            alerter.write(f"[ALERT] {ts} {id} temp={temp} - ABNORMAL\n")
        
    except Exception as e:
        print(f"exception: {e}")
    logger.close()
    alerter.close()

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
    client.disconnect()



