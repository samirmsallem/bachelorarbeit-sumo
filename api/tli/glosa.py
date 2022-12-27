from api.rest import client


def glosa_for_position(latitude, longitude, bearing, speed):
    response = client.perform_request(latitude, longitude, bearing, speed)

    if(response == None):
        return glosa_for_position(latitude, longitude, bearing, speed)
    
