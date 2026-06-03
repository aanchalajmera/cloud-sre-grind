import csv
import json
from datetime import datetime

# Simulate beacon data coming from PAGOS
# In reality this will be real data from Parikshit
sample_beacons = [
    {"timestamp": "2026-06-03T08:00:00Z", "battery_voltage": 7.8, "temperature": 22.1, "rssi": -85, "solar_current": 1.2},
    {"timestamp": "2026-06-03T08:10:00Z", "battery_voltage": 7.6, "temperature": 23.4, "rssi": -88, "solar_current": 1.1},
    {"timestamp": "2026-06-03T08:20:00Z", "battery_voltage": 6.2, "temperature": 38.5, "rssi": -95, "solar_current": 0.3},
    {"timestamp": "2026-06-03T08:30:00Z", "battery_voltage": 7.9, "temperature": 21.0, "rssi": -82, "solar_current": 1.4},
    {"timestamp": "2026-06-03T08:40:00Z", "battery_voltage": 5.8, "temperature": 42.0, "rssi": -101, "solar_current": 0.1},
]

# Health thresholds
THRESHOLDS = {
    "battery_voltage": {"min": 6.5, "max": 8.4},
    "temperature":     {"min": -10, "max": 40},
    "rssi":            {"min": -100, "max": 0},
    "solar_current":   {"min": 0.2, "max": 2.0},
}

def check_parameter(name, value):
    t = THRESHOLDS[name]
    if value < t["min"] or value > t["max"]:
        return "ANOMALY"
    return "NOMINAL"

def parse_beacon(beacon):
    print(f"\n--- Beacon at {beacon['timestamp']} ---")
    alerts = []
    for key in THRESHOLDS:
        status = check_parameter(key, beacon[key])
        print(f"  {key}: {beacon[key]} → {status}")
        if status == "ANOMALY":
            alerts.append(f"ALERT: {key} = {beacon[key]} is out of range")
    
    if alerts:
        for alert in alerts:
            print(f"  ⚠️  {alert}")
    else:
        print("  ✅ All systems nominal")

# Write to CSV log
def save_to_csv(beacons, filename="telemetry_log.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=beacons[0].keys())
        writer.writeheader()
        writer.writerows(beacons)
    print(f"\nTelemetry log saved to {filename}")

# Run the parser
print("PARIKSHIT-1 TELEMETRY PARSER")
print("="*40)
for beacon in sample_beacons:
    parse_beacon(beacon)

save_to_csv(sample_beacons)

# Read it back
print("\nReading back from CSV:")
with open("telemetry_log.csv", "r") as f:
    print(f.read())
