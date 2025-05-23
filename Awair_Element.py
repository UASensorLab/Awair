import http.client
import json
import time
import csv
from datetime import datetime

# Replace with your Awair Element's local IP address or mDNS hostname.
DEVICE_HOST = "192.000.0.000"  # e.g., "awair-elem-56cd78.local"
DEVICE_ID = "xxxxx"
DEVICE_TYPE = "awair-element"  # For an Awair Element

# CSV file where the data will be logged.
CSV_FILENAME = "awair_local_data.csv"

# Fieldnames for all the sensor values you provided.
FIELDNAMES = [
    "timestamp",
    "score",
    "dew_point",
    "temp",
    "humid",
    "abs_humid",
    "co2",
    "co2_est",
    "co2_est_baseline",
    "voc",
    "voc_baseline",
    "voc_h2_raw",
    "voc_ethanol_raw",
    "pm25",
    "pm10_est"
]

def get_latest_air_data():
    conn = http.client.HTTPConnection(DEVICE_HOST)
    conn.request("GET", "/air-data/latest")
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    conn.close()
    return data

def init_csv(filename, fieldnames):
    # Create CSV file with headers if it doesn't already exist.
    try:
        with open(filename, mode='x', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        print(f"Created new CSV file: {filename}")
    except FileExistsError:
        print(f"CSV file {filename} already exists. Appending data.")

def log_data_to_csv(filename, fieldnames, data_row):
    # Append a single row to the CSV file.
    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data_row)

if __name__ == "__main__":
    init_csv(CSV_FILENAME, FIELDNAMES)
    
    print("Starting data logging. Press Ctrl+C to stop.")
    try:
        while True:
            raw_data = get_latest_air_data()
            try:
                parsed = json.loads(raw_data)
                # Build a row using all the sensor keys.
                data_row = {
                    "timestamp": parsed.get("timestamp", datetime.utcnow().isoformat()),
                    "score": parsed.get("score", None),
                    "dew_point": parsed.get("dew_point", None),
                    "temp": parsed.get("temp", None),
                    "humid": parsed.get("humid", None),
                    "abs_humid": parsed.get("abs_humid", None),
                    "co2": parsed.get("co2", None),
                    "co2_est": parsed.get("co2_est", None),
                    "co2_est_baseline": parsed.get("co2_est_baseline", None),
                    "voc": parsed.get("voc", None),
                    "voc_baseline": parsed.get("voc_baseline", None),
                    "voc_h2_raw": parsed.get("voc_h2_raw", None),
                    "voc_ethanol_raw": parsed.get("voc_ethanol_raw", None),
                    "pm25": parsed.get("pm25", None),
                    "pm10_est": parsed.get("pm10_est", None)
                }
                log_data_to_csv(CSV_FILENAME, FIELDNAMES, data_row)
                print(f"Logged data at {datetime.utcnow().isoformat()}")
            except Exception as e:
                print("Error parsing data:", e)
                print("Raw response:", raw_data)
            # Poll every 10 seconds (adjust as needed)
            time.sleep(60)
    except KeyboardInterrupt:
        print("Data logging stopped.")

