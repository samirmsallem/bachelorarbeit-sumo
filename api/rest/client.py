import requests
import sys


def perform_request(latitude, longitude, bearing, speed=50):
    '''
    Restclient that will perform a post request to the local backend to receive information about the traffic light

    Exemplary response can be found in /root/docs/backend_response.json

    '''
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
            return response.json()
        else:
            print("Request failed with status code: ", response.status_code, response.json())
            return None

    except ConnectionError as e:
       print(e.args[0].reason.errno) 
       sys.exit("Unable to perform request to local backend")
