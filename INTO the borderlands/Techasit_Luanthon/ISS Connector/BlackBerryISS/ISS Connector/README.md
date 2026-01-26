# ISS Connector

This project demonstrates how to connect to **public International Space Station (ISS) data feeds**
and retrieve:

- Real-time ISS location (updates every 5 seconds)
- Current astronauts aboard the ISS

## APIs Used
- Open Notify ISS API (public, no API key required)

## How to Run
```bash
pip install -r requirements.txt
python main.py
```

The application will print the current crew members and then continuously update the ISS coordinates. Press `Ctrl+C` to stop the tracking.

## Disclaimer
This project connects to **public informational APIs only**.
It does NOT connect to internal or secure NASA/ISS systems.
