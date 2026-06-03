# Data types you'll use constantly
satellite_id = "PARIKSHIT-1"
battery_voltage = 7.4
is_healthy = True
subsystems = ["COMMS", "EPS", "ADCS", "OBC"]

# Dictionary - this is how telemetry data is structured
beacon = {
    "timestamp": "2026-06-03T08:48:00Z",
    "battery_voltage": 7.4,
    "temperature": 23.5,
    "rssi": -87,
    "is_healthy": True
}

# Accessing dictionary values
print(f"Satellite: {satellite_id}")
print(f"Battery: {beacon['battery_voltage']}V")
print(f"Temperature: {beacon['temperature']}C")
print(f"Signal strength: {beacon['rssi']}dBm")

# Basic health check function
def check_health(voltage, temp):
    if voltage < 6.5:
        return "CRITICAL - Low battery"
    elif temp > 40:
        return "WARNING - High temperature"
    else:
        return "NOMINAL"

status = check_health(beacon['battery_voltage'], beacon['temperature'])
print(f"Status: {status}")
