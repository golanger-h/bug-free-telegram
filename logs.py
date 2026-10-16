def generate_log(json_info: dict) -> str:
    """ generate log string from json data """
    try:
        ts = json_info.get("ts", "")
        id = json_info.get("device_id", "")
        temp = json_info.get("temperature", "")
        hum = json_info.get("humidity", "")
        return f"[{ts}] {id} temp={temp} hum={hum}\n"
    except Exception as e:
        print(f"Exception: {e}")
        return ""

def generate_alert(json_info: dict) -> str:
    """ generate alert string from json data """
    try:
        ts = json_info.get("ts", "")
        id = json_info.get("device_id", "")
        temp = json_info.get("temperature", "")
        return f"[ALERT] {ts} {id} temp={temp} - ABNORMAL\n"
    except Exception as e:
        print(f"Exception: {e}")
        return ""
