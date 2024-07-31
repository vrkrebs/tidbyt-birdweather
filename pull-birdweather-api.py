#!/usr/bin/env python
import requests
import json
from datetime import datetime, timedelta, timezone

def get_species_data(station, token, hours):
    hours_ago = datetime.now(timezone.utc) - timedelta(hours=hours)
    since = hours_ago.isoformat()
    print("Bird count since(UTC):", since)
    url = f"https://app.birdweather.com/api/v1/stations/{station}/species?period=day&since={since}"
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)
    data = response.json()

    if "species" in data:
        for species in data["species"]:
            print(species["commonName"], species["detections"]["total"])
    else:
        print("Key 'species' not found in the response data.")


def get_last_5_detections(station, token):
    url = f"https://app.birdweather.com/api/v1/stations/{station}/detections"
    params = {
        "limit": 10,
        "order": "desc"
    }
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # print the list for debugging so we see the top 10, including duplicates
    ##########################################################################
    if "detections" in data:
        for detection in data["detections"]:
            print(detection["species"]["commonName"], detection["timestamp"])
    else:
        print("Key 'detections' not found in the response data.")
    print("\n")
    ##########################################################################
    if "detections" in data:
        species_count = {}
        species_timestamps = {}
        for detection in data["detections"]:
            species_name = detection["species"]["commonName"]
            timestamp = detection["timestamp"]
            # make timestamp human readable and timezone aware so it prints the time local to the station
            # timestamp = datetime.fromisoformat(timestamp).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            timestamp = datetime.fromisoformat(timestamp).astimezone().strftime("%H:%M:%S %Z")

            if species_name in species_count:
                species_count[species_name] += 1
            else:
                species_count[species_name] = 1
                # also track the timestamp for the first detection of each species
                species_timestamps[species_name] = timestamp

        for species_name, count in species_count.items():
            timestamp = species_timestamps[species_name]
            if count > 1:
                print(f"{species_name} {timestamp} *")
            else:
                print(f"{species_name} {timestamp}")
    else:
        print("Key 'detections' not found in the response data.")

if __name__ == "__main__":

    # Read the token from the config file
    with open('config.json') as config_file:
        config = json.load(config_file)
        token = config["token"]
        station = config["station"]

    # get_species_data(station, token, 6)
    get_last_5_detections(station, token)
