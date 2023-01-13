import requests
import sys
import json

OFFLINE_MODE = True
STORE = False

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

    if OFFLINE_MODE:
        return previously_stored_response()

    try: 
        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            response_json = response.json()

            if STORE:
                with open(f"api/rest/scenario1/{response_msg}.json", "w") as outfile:
                    json.dump(response_json, outfile)
                
                response_msg += 1

            return response_json
        
        else:
            return None

    except requests.RequestException:
        sys.exit("Unable to perform request to local backend")


def previously_stored_response():
    global response_msg

    if response_msg == 73:
        sys.exit("Stored simulation ended!")

    with open(f"api/rest/scenario1/{response_msg}.json", "r") as infile:
        loaded_response = json.load(infile)
    
    response_msg += 1

    return loaded_response
