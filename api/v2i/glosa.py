import traci
from api.rest import client
from api.v2i import traffic_light as tli_helper
from api.output import logger
from api.sim import helper
from api.v2i import tli


tli_store = tli.TrafficLightInformation()

def parse_justification(justification):
    return justification.replace("[Green]", "g").replace("Green", "g").replace("Red", "r").replace("->", "").replace(" ", "")


def get_justification(glosa):
    return glosa["justification"]


def get_recommended_speed(glosa):
    return glosa["recommendation"]


def get_minimum_speed(glosa):
    return glosa["minimumSpeed"]


def get_maximum_speed(glosa):
    return glosa["maximumSpeed"]


def improve_vehicle_speed(receiver, distance_to_last_vehicle):
    time, receiver, distance, glosa, signals = tli_store.read(receiver)
    age = traci.simulation.getTime() - time

    reason = parse_justification(get_justification(glosa))

    if get_minimum_speed(glosa) < get_recommended_speed(glosa):
        new_speed = distance_to_last_vehicle / time

        if new_speed >= get_minimum_speed(glosa):
            traci.vehicle.setSpeed(receiver, new_speed)
            print(f"Reduced vehicle speed from {get_recommended_speed(glosa)} to {new_speed * 3.6}")

    
    


def glosa_for_position(latitude, longitude, bearing, speed):
    response = client.perform_request(latitude, longitude, bearing, speed)
    
    if(response == None or response["signals"] == None or response["signals"][0]["glosa"] == None):
        return glosa_for_position(latitude, longitude, bearing, speed)
        
    return [response["signals"][0]["glosa"], response["distanceToStopLine"], tli_helper.extract_tli(response["signals"])];


def move_according_to_glosa(vehicle):
    if helper.vehicle_did_not_cross_intersection(vehicle):
        x, y = traci.vehicle.getPosition(vehicle)
        long, lat = traci.simulation.convertGeo(x, y)
        angle = traci.vehicle.getAngle(vehicle)

        glosa, distance, signals = glosa_for_position(lat, long, angle, 30)
        tli_store.write(traci.simulation.getTime(), vehicle, distance, glosa, signals)
        speed = get_recommended_speed(glosa)
        decision = get_justification(glosa)
        logger.printlog("###### Vehicle " + vehicle + " ######")
        logger.printlog("Calculated speed: " + str(speed) + " km/h with recommendation: " + decision)
        traci.vehicle.setSpeed(vehicle, speed / 3.6)
    else:
        traci.vehicle.setSpeed(vehicle, -1) # give vehicle controls back to simulation if vehicle crossed intersection
    
