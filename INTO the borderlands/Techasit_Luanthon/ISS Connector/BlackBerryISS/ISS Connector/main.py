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
    try:
        r = requests.get(ISS_LOCATION_API, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data["iss_position"]
    except requests.RequestException as e:
        print(f"Error fetching location: {e}")
        return None

def get_iss_crew():
    try:
        r = requests.get(ISS_CREW_API, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data["people"]
    except requests.RequestException as e:
        print(f"Error fetching crew: {e}")
        return []

def track_iss():
    print("Connecting to International Space Station data feeds...")
    
    # Get crew once
    crew = get_iss_crew()
    if crew:
        print(f"\nCrew on board ISS ({len(crew)}):")
        for person in crew:
            # Handle cases where 'craft' might be missing, though usually present
            craft = person.get('craft', 'ISS')
            print(f"- {person['name']} (Craft: {craft})")
    else:
        print("Could not retrieve crew information.")
    
    print("\nStarting real-time location tracking (Ctrl+C to stop)...")
    try:
        while True:
            location = get_iss_location()
            if location:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp}] ISS Location - Lat: {location['latitude']}, Lon: {location['longitude']}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nTracking stopped.")

if __name__ == "__main__":
    track_iss()
