import os
import time
import psycopg2
import random
from prometheus_client import start_http_server, Gauge, Counter

# Prometheus metrics
battery_gauge = Gauge('satwatch_battery_voltage', 'Battery voltage in volts')
temp_gauge = Gauge('satwatch_temperature', 'Temperature in celsius')
rssi_gauge = Gauge('satwatch_rssi', 'Signal strength in dBm')
solar_gauge = Gauge('satwatch_solar_current', 'Solar current in amps')
anomaly_counter = Counter('satwatch_anomalies_total', 'Total anomalies detected')
beacon_counter = Counter('satwatch_beacons_total', 'Total beacons processed')

# Database config
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
    "dbname": os.getenv("DB_NAME", "telemetry"),
    "user": os.getenv("DB_USER", "parikshit"),
    "password": os.getenv("DB_PASSWORD", "satellite123")
}

THRESHOLDS = {
    "battery_voltage": {"min": 6.5, "max": 8.4},
    "temperature":     {"min": -10, "max": 40},
    "rssi":            {"min": -100, "max": 0},
    "solar_current":   {"min": 0.2,  "max": 2.0},
}

def connect_db():
    print("Connecting to database...")
    for i in range(10):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            print("Connected successfully")
            return conn
        except Exception as e:
            print(f"Attempt {i+1}/10 failed: {e}")
            time.sleep(3)
    raise Exception("Could not connect to database")

def setup_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ DEFAULT NOW(),
                battery_voltage FLOAT,
                temperature FLOAT,
                rssi FLOAT,
                solar_current FLOAT,
                status VARCHAR(20)
            )
        """)
        conn.commit()
    print("Table ready")

def check_health(beacon):
    for key, val in beacon.items():
        t = THRESHOLDS[key]
        if val < t["min"] or val > t["max"]:
            return "ANOMALY"
    return "NOMINAL"

def insert_beacon(conn, beacon):
    status = check_health(beacon)
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO telemetry 
            (battery_voltage, temperature, rssi, solar_current, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            beacon["battery_voltage"],
            beacon["temperature"],
            beacon["rssi"],
            beacon["solar_current"],
            status
        ))
        conn.commit()

    # Update Prometheus metrics
    battery_gauge.set(beacon["battery_voltage"])
    temp_gauge.set(beacon["temperature"])
    rssi_gauge.set(beacon["rssi"])
    solar_gauge.set(beacon["solar_current"])
    beacon_counter.inc()
    
    if status == "ANOMALY":
        anomaly_counter.inc()
    
    print(f"Beacon stored → {status} | battery={beacon['battery_voltage']}V temp={beacon['temperature']}C")

def main():
    # Start Prometheus metrics server
    start_http_server(8000)
    print("Prometheus metrics server started on port 8000")
    
    print("SATWATCH TELEMETRY PARSER")
    print("="*40)
    conn = connect_db()
    setup_table(conn)
    
    iteration = 0
    while True:
        iteration += 1
        beacon = {
            "battery_voltage": round(random.uniform(5.5, 8.4), 2),
            "temperature": round(random.uniform(15.0, 45.0), 2),
            "rssi": round(random.uniform(-105, -75), 2),
            "solar_current": round(random.uniform(0.0, 2.0), 2),
        }
        insert_beacon(conn, beacon)
        time.sleep(5)

if __name__ == "__main__":
    main()
