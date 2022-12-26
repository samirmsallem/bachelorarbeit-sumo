import requests


def perform_request(latitude, longitude, bearing):
    url = "http://localhost:8080/api/predictions"

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "latitude": latitude,
        "longitude": longitude,
        "direction": bearing,
        "currentSpeed": "50",
        "considerTraffic": "false"
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return response
    else:
        print("Request failed with status code:", response.status_code)
        return None

def get_approach_signal(approachId):
    switch case
