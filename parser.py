import random as rnd
import json as js
import datetime as dt

def is_anomaly(info: dict) -> bool:
    """ check anomaly on sensor data """
    try:
        return info.get("alerts", False) == True
    except Exception as e:
        print(f"Exception: {e}")
        return False

def pars_json_from_decoded_payload(payload: str) -> dict:
    """ parse json data from sensor """

    if payload == "":
        return {"rc": -1}

    try:
        return js.loads(payload)
    except Exception as e:
        print(f"Exception: {e}")
        return {"rc": -1}

def data_generator(id: str):
    """ generate json data for sensor """

    current_temperature = rnd.uniform(20, 30) 
    anomaly = rnd.uniform(0,20)
    is_anomaly = False
    json_dumped = {}
    if anomaly > 13:
        current_temperature = -5 
        is_anomaly = True
        json_dumped = {
            "device_id": id,
            "temperature": -5,
            "humidity": 45.2,
            "unit": "C",
            "ts": dt.datetime.now().isoformat(),
            "alerts": True
            }
    else:
        json_dumped = {
                "device_id": id,
                "temperature": 22.5,
                "humidity": 45.2,
                "unit": "C",
                "ts": dt.datetime.now().isoformat(),
                }
    return js.dumps(json_dumped)