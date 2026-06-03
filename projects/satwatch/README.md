# SatWatch — Satellite Ground Station Monitor

A real-time telemetry monitoring platform for student nanosatellite 
ground stations. Built to solve a real problem: most student satellite 
teams receive beacon data as raw logs with no live visibility into 
satellite health.

## What it does
- Parses beacon frames received at a ground station
- Detects anomalies in battery voltage, temperature, RSSI, 
  and solar current in real time
- Stores all telemetry in a PostgreSQL time-series database
- Displays live dashboards via Grafana with automatic alerting

## Architecture
## Stack
- Python 3.12 — beacon parser and anomaly detection
- PostgreSQL 15 — time-series telemetry storage  
- Grafana 13 — live dashboards and alerting
- Docker + Docker Compose — containerised deployment
- AWS EC2 — cloud hosting (coming soon)
- Terraform — infrastructure as code (coming soon)

## Run locally
```bash
git clone https://github.com/aanchalajmera/cloud-sre-grind
cd cloud-sre-grind/projects/satwatch
docker compose up --build
```

Open http://localhost:3000 (admin / parikshit123)

## Who is this for
Any student satellite team that wants real-time visibility into 
their ground station telemetry. Designed to work with standard 
UHF/VHF beacon formats used by most nanosatellite projects.

## Author
Aanchal Ajmera — MIT Manipal  
github.com/aanchalajmera
