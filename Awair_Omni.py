import http.client
import json
import time
import csv
import os
from datetime import datetime, timezone


# Ensure the Data folder exists
DATA_DIR = "Data"
os.makedirs(DATA_DIR, exist_ok=True)

# List your devices: host, CSV filename, and device_type
DEVICES = [
    {"host": "192.168.0.97", "csv": os.path.join(DATA_DIR, "omni_Room3141.csv"), "DEVICE_TYPE": "awair-omni", "DEVICE_ID": "127D3D"},
    {"host": "192.168.0.228", "csv": os.path.join(DATA_DIR, "omni_Room3141B.csv"), "DEVICE_TYPE": "awair-omni", "DEVICE_ID": "12490F"},
]

# Include device_type as its own column
FIELDNAMES = [
    "time",
    "temp",
    "score",
    "humid",
    "co2",
    "voc",
    "pm25",
    "lux",
    "spl_a"
]

def get_latest(host):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", "/air-data/latest")
    resp = conn.getresponse()
    data = resp.read().decode()
    conn.close()
    return data

def init_csv(filename, fieldnames):
    try:
        with open(filename, mode='x', newline='') as f:
            csv.DictWriter(f, fieldnames=fieldnames).writeheader()
    except FileExistsError:
        pass

def log_csv(filename, fieldnames, row):
    with open(filename, mode='a', newline='') as f:
        csv.DictWriter(f, fieldnames=fieldnames).writerow(row)

if __name__ == "__main__":
    # Create CSVs with headers
    for dev in DEVICES:
        init_csv(dev["csv"], FIELDNAMES)

    print("Starting data logging for all devices. Ctrl+C to stop.")
    try:
        while True:
            now_utc = datetime.now(timezone.utc).isoformat()
            for dev in DEVICES:
                raw = get_latest(dev["host"])
                try:
                    obj = json.loads(raw)
                    row = {
                        "time":        obj.get("timestamp", now_utc),
                        "temp":        obj.get("temp"),
                        "score":       obj.get("score"),
                        "humid":       obj.get("humid"),
                        "co2":         obj.get("co2"),
                        "voc":         obj.get("voc"),
                        "pm25":        obj.get("pm25"),
                        "lux":         obj.get("lux"),
                        "spl_a":       obj.get("spl_a")
                    }
                    log_csv(dev["csv"], FIELDNAMES, row)
                    print(f"[{dev['DEVICE_ID']}] Logged at {row['time']}")
                except Exception as e:
                    print(f"[{dev['host']}] Parse error:", e)
            time.sleep(60)
    except KeyboardInterrupt:
        print("Stopped logging.")
