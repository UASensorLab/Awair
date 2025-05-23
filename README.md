# Awair Data Collection Guide

This guide explains how to collect air quality data from your Awair devices. You have two primary approaches depending on your device type and data needs:

## 1. Export Data via the Awair Dashboard
- **Method:**  
  From [dashboard.awair.com](https://dashboard.awair.com), you can export data for any selected time window at 5-minute intervals.
- **Steps:**
  - Navigate to **Awair Dashboard > Export Data**.
  - Select your desired time interval.
  - Download the provided ZIP file (which contains a CSV file with your data).

## 2. Programmatic Data Collection for Finer Intervals
To extract data at intervals shorter than 5 minutes (as low as 10 seconds), you have three options:

### (a) Use the Provided `awair_collectData.js` Script
- **Description:**  
  This Node.js script is designed to save a single CSV file containing data for any time window at intervals as short as 10 seconds.
- **Important Notes:**
  - To prevent denial-of-service (DOS) attacks, Awair limits the number of data entries you can extract in one minute.
  - The script automatically pauses for 60 seconds after collecting 10 hours’ worth of data, so extracting data over several days may require additional time.

### (b) Write Your Own Script Using Examples
- **Resources:**  
  Use the examples from `exampleRequests.js` or refer to the [Awair Cloud API Documentation](https://docs.dashboard.getawair.com/).
- **Considerations:**
  - The base example typically fetches 1 hour’s worth of data.
  - To collect a longer time window, you can adapt the code to loop through multiple 1-hour segments.

### (c) Local-Network Logging from Awair Omni Devices
- **Description:**  
  For on-premise setups or when you need sub-minute resolution without cloud calls, you can poll your Omni’s local API and write directly to CSV.
- **Features:**
  - Simultaneously log from multiple Omni units.
  - Automatically creates a `Data/` folder to store each device’s CSV.
  - Tags every row with **device_type** and **device_id** for easy identification.
- **Quick Start:**
  1. Clone or copy the Python script `awair_omni.py`.
  2. In the `DEVICES` list, specify each Omni’s `host` IP, target CSV (under `Data/`), `device_type` (“awair-omni”), and its unique `device_id`.
  3. Run:
     ```bash
     python awair_omni.py
     ```
  4. The script will:
     - Ensure a `Data/` directory exists.
     - Create each CSV with headers (`time,temp,score,humid,co2,voc,pm25,lux,spl_a`).
     - Poll `/air-data/latest` every 60 seconds.
     - Append a row for each device into its own CSV.

---

## Configuration Details

### For Awair Omni Devices (Using the Cloud API)
If you are using an Awair Omni device, your script will interact with the cloud API. Configure the following parameters:

- **API Key:**  
  - **What It Is:** Your unique API token provided by Awair.  
  - **Usage:** This is used in the `Authorization` header of your API requests (formatted as `Bearer <API_KEY>`).

- **Device ID:**  
  - **What It Is:** The unique identifier for your device.  
  - **Usage:** Include the device ID in the API endpoint URL.
  
- **Device Type:**  
  - **Typical Value:** For an Awair Omni, it might be `"awair-omni"`.  
  - **Usage:** Used in the URL to specify the device type.

- **Organization ID (OrgID):**  
  - **What It Is:** Some devices require an OrgID (organization identifier) if they are part of a managed or enterprise setup.  
  - **Usage:** This will appear in the endpoint URL (e.g., `/v1/orgs/<ORG_ID>/devices/...`).  
  - **Note:** If your device does not have an organization (for example, an Awair Element), you will use a different endpoint (see below).

- **API Endpoint Host:**  
  - **Value for Cloud API:** `developer-apis.awair.is`  
  - **Query Parameters:** When retrieving historical (raw) data, you’ll set parameters such as:
    - `from`: Start timestamp (ISO8601 format)
    - `to`: End timestamp (ISO8601 format)
    - `limit`: Maximum number of entries (e.g., 360 for 10-second intervals)
    - `desc`: Boolean for descending order
    - `fahrenheit`: Boolean to select Fahrenheit (or Celsius)

### For Awair Element Devices (Using the Local API)
For an Awair Element, the device exposes a local API that only supplies current sensor readings:
- **Local API Characteristics:**  
  - No API key is required.  
  - The device does not store historical data. To build a historical dataset, you must continuously log the data.
  
- **Configuration Items:**
  - **Host:**  
    - Use your device’s local IP address or its mDNS hostname (e.g., `192.168.0.125` or `awair-elem-56cd78.local`).
  - **Endpoint:**  
    - The only available endpoint is `/air-data/latest`.
  - **Polling Interval:**  
    - Set your script to poll this endpoint (e.g., every 10 seconds or 60 seconds) and write the returned sensor data (including keys like `timestamp`, `score`, `dew_point`, `temp`, `humid`, `abs_humid`, `co2`, `co2_est`, `co2_est_baseline`, `voc`, `voc_baseline`, `voc_h2_raw`, `voc_ethanol_raw`, `pm25`, and `pm10_est`) to a CSV file.

---

## Summary

- **Dashboard Export (Awair Omni):**  
  Quick method to export 5-minute interval data using the web dashboard.

- **Programmatic Collection:**  
  - For **Awair Omni** (Cloud API), supply your API Key, Device ID, Device Type (e.g., `awair-omni`), and OrgID in the endpoint URL. Use query parameters to select a time window and data granularity.  
  - For **Awair Omni** (Local API), use the provided Python logger to poll multiple Omnis, write into `Data/` CSVs, and tag each row with `device_type` & `device_id`.  
  - For **Awair Element** (Local API), use the device’s local IP/hostname and the `/air-data/latest` endpoint to log real-time data. For historical data, you must log continuously.

For further assistance, please contact the UA Sensor Lab. If you borrowed the device, they can provide you with the necessary credentials (DeviceID, OrgID, and API Key) for cloud-based data extraction.

