import requests
import json


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
        "considerTraffic": "false",
        "asTurns": "false"
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed with status code: ", response.status_code, response.json())
        return None


def get_approach_signal(approachId):
    if approachId == 1:
        return perform_request(48.76280618764156, 11.427623411273599, 105.4492514593)["signals"]
    elif approachId == 2:
        return perform_request(48.763513657462475, 11.431514833553978, 235.909123032)["signals"]
    else:
        return perform_request(48.758733700993886, 11.425519395220782, 40.2685517938)["signals"]


def extract_tli(signals):
    phases = []
    count = len(signals[0]["predictions"])
    predictions = signals[0]["predictions"]

    if(count == 0):
        return None
    else:
        phases.append([signals[0]["bulbColor"], predictions[0]["timeToChange"], predictions[0]["confidence"]])
        if(count == 2):
            phases.append([predictions[0]["bulbColor"], predictions[1]["timeToChange"] - predictions[0]["timeToChange"], predictions[1]["confidence"]])
        return phases


def pretty_print_tli(phases):
    print("Received program for approach signal head:")
    for phase in phases:
        print(phase[0] + " phase for " + str(phase[1]) + "seconds. Confidence: " + str(phase[2]) + "%")


def main():
    signals = get_approach_signal(3)
    pretty_print_tli(extract_tli(signals))


if __name__ == "__main__":
    main()