from api.rest import client


def glosa_for_position(latitude, longitude, bearing, speed):
    response = client.perform_request(latitude, longitude, bearing, speed)
    
    if(response == None or response["signals"] == None or response["signals"][0]["glosa"] == None):
        return glosa_for_position(latitude, longitude, bearing, speed)

    glosa = response["signals"][0]["glosa"]

    return [glosa["recommendation"], glosa["justification"]];
    