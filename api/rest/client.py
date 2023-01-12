import requests
import sys
import json

OFFLINE_MODE = False

response_msg = 0


def perform_request(latitude, longitude, bearing, speed=50):
    '''
    Restclient that will perform a post request to the local backend to receive information about the traffic light

    Exemplary response can be found in /root/docs/backend_response.json

    '''

    global response_msg

    url = "http://localhost:8080/api/predictions"

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "latitude": latitude,
        "longitude": longitude,
        "direction": bearing, 
        "currentSpeed": speed,
        "considerTraffic": "false", # disabled as this would take the traffic information from the google api (not reliable/reproducable in simulation)
        "asTurns": "false"
    }

    try: 
        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            response_json = response.json()

            if OFFLINE_MODE:
                with open(f"api/rest/dump/{response_msg}.json", "w") as outfile:
                    json.dump(response_json, outfile)
                
                response_msg += 1

            return response_json

        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Unable to perform request to local backend, reason: {e}")
        return previously_stored_response(response_msg)


def previously_stored_response(response_msg):

    with open(f"api/rest/dump/{response_msg}.json", "w", "r") as infile:
        loaded_response = json.load(infile)
    response_msg += 1

    return loaded_response
