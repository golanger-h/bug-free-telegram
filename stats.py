import threading

def generate_stat(info: dict, stats: dict) -> bool:
    try:    
        "generate stat string from json data"
        id = info.get("device_id", "NOT_FOUND")
        temp = info.get("temperature", "NOT FOUND")
        ts = info.get("ts", "NOT FOUND")
        if "avg" in stats and id in stats["avg"]:
            if "alltmp" in stats["avg"][id]:
                stats["avg"][id]["alltmp"] += temp
            else:
                stats["avg"][id]["alltmp"] = temp
            if "count" in stats["avg"][id]:
                stats["avg"][id]["count"] += 1
            else:
                stats["avg"][id]["count"] = 1
        else:
            if "avg" in stats:
                stats["avg"][id] = {"alltmp": temp, "count": 1}
        if "alerts" in info:
            stats["alerts"] += 1
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False
    
def print_stat(stats: dict) -> bool:
    try:
        print("-"*3 + "STATS" + "-"*3)
        print(f"Total messages: {stats.get('total', -1)}")
        print(f"Alerts: {stats.get('alerts', -1)}")
        print("Avg temp per zone:")
        if 'avg' in stats:
            for zone, temp in stats['avg'].items():
                print(f"\t{zone}: {temp['alltmp'] / temp['count'] if temp['count'] != 0 else 1}")
        print("-"*3 + "-----" + "-"*3)
        threading.Timer(10.0, print_stat, args=(stats,)).start()
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False