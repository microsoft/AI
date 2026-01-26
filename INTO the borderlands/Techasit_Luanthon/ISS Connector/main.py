
"""
ISS Connector
Connects to public International Space Station (ISS) data APIs.
Data sources:
- Open Notify (ISS current location & crew)
"""

import requests
import time

ISS_LOCATION_API = "http://api.open-notify.org/iss-now.json"
ISS_CREW_API = "http://api.open-notify.org/astros.json"

def get_iss_location():
    r = requests.get(ISS_LOCATION_API, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["iss_position"]

def get_iss_crew():
    r = requests.get(ISS_CREW_API, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["people"]

if __name__ == "__main__":
    print("Connecting to International Space Station data feeds...")
    location = get_iss_location()
    crew = get_iss_crew()

    print(f"ISS Latitude : {location['latitude']}")
    print(f"ISS Longitude: {location['longitude']}")
    print("\nCrew on board ISS:")
    for person in crew:
        print("-", person["name"])

    print("\nData fetch successful.")
