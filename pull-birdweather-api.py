#!/usr/bin/env python
import requests
import json
from datetime import datetime, timedelta, timezone

# get config data from user input and write it to a file
def build_config():
    token = input("Enter the token: ")
    station = input("Enter the station: ")

    config = {
        "token": token,
        "station": station
    }

    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# get the bird count for the last x hours
def get_species_data(station, token, hours):
    hours_ago = datetime.now(timezone.utc) - timedelta(hours=hours)
    since = hours_ago.isoformat()
    print(f"Bird count at stations {station} looking back {hours} hours - jsince(UTC):", since)
    url = f"https://app.birdweather.com/api/v1/stations/{station}/species?period=day&since={since}"
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)
    data = response.json()

    if "species" in data:
        # print(f"Species at {station} detected in the last {hours} hours:")
        for species in data["species"]:
            print(species["commonName"], species["detections"]["total"])
    else:
        print("Key 'species' not found in the response data.")


def get_last_few_detections(station, token, limit, unique_requested):
    url = f"https://app.birdweather.com/api/v1/stations/{station}/detections"
    params = {
        "limit": limit,     # limit is how many to return
        "order": "desc"          # order is desc for most recent first
    }
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if unique_requested:
        # last x detections and timestamps for unique species
        print(f"Unique species detected in the last {limit} detections:")  
        print(f"Birds marked with a * were detected more than once.")     
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
    else:
        # last x detections and timestamps for all species
        print(f"Species detected in the last {limit} detections:") 
        if "detections" in data:
            for detection in data["detections"]:
                print(detection["species"]["commonName"], detection["timestamp"])
        else:
            print("Key 'detections' not found in the response data.\n")
        # print("\n")

##########################################################################
if __name__ == "__main__":

    # if the config file doesn't exist, create it by running the build_config function
    try:
        with open('config.json') as config_file:
            pass
    except FileNotFoundError:
        build_config()

    # Read the token from the config file
    with open('config.json') as config_file:
        config = json.load(config_file)
        token = config["token"]
        station = config["station"]

    # get the bird count for the last 6 hours
    get_species_data(station, token, 6)
    print("\n")
    # get the last x (limit) detections and timestamps
    get_last_few_detections(station, token, limit=5, unique_requested=False)
    print("\n")
    # get the last x (limit) detections and timestamps (limit max value by API: 100)
    get_last_few_detections(station, token, limit=100, unique_requested=True)
    