import traci
from api.rest import client
from api.v2i import traffic_light as tli_helper
from api.output import logger
from api.sim import helper
from api.v2i import tli
from api.sim import visualizer


tli_store = tli.TrafficLightInformation()

influenced_vehicles = []


def parse_justification(justification):
    '''Parses the justification (reason for glosa decision based on signal head phases) into a simple character list'''
    return justification.replace("[Green]", "g").replace("Green", "g").replace("Red", "r").replace("->", "").replace(" ", "")


def get_justification(glosa):
    '''Returns the justification of the provided glosa object'''
    return glosa["justification"]


def get_recommended_speed(glosa):
    '''Returns the recommended speed of the provided glosa object'''
    return glosa["recommendation"]


def get_minimum_speed(glosa):
    '''Returns the minimum speed of the provided glosa object'''
    return glosa["minimumSpeed"]


def get_maximum_speed(glosa):
    '''Returns the maximum speed of the provided glosa object'''
    return glosa["maximumSpeed"]


def improve_vehicle_speed(receiver, distance_to_last_vehicle):
    '''Improves the vehicle speed of a glosa influenced vehicle based on received vehicle positions (based on v2v communication)'''
    time, receiver, distance, glosa, signals = tli_store.read(receiver)
    age = traci.simulation.getTime() - time

    reason = parse_justification(get_justification(glosa))

    if get_minimum_speed(glosa) < get_recommended_speed(glosa):
        if signals[0][0] == 'Red' and (signals[0][1] - age) >= 0:
            ttg = signals[0][1] - age
            green_end = signals[1][1] if len(signals) > 1 else 10
            min_speed = distance_to_last_vehicle / (ttg + green_end)
            max_speed = distance_to_last_vehicle / (ttg + 1)
            if max_speed * 3.6 > 50:
                max_speed = 45 / 3.6
            traci.vehicle.setSpeed(receiver, max_speed)
            influenced_vehicles.append([receiver, min_speed, max_speed])
            print(f"Changed vehicle speed of {receiver} from {get_recommended_speed(glosa)} km/h to {max_speed * 3.6} km/h")
            return ttg
    

def glosa_exists(vehicle):
    '''Checks whether the provided vehicle has requests the glosa already'''
    return tli_store.read(vehicle) != None


def glosa_for_position(latitude, longitude, bearing, speed):
    '''Returns the GLOSA for a provided position and speed'''
    response = client.perform_request(latitude, longitude, bearing, speed)
    
    if(response == None or response["signals"] == None or response["signals"][0]["glosa"] == None):
        return [None, None, None]
        
    return [response["signals"][0]["glosa"], response["distanceToStopLine"], tli_helper.extract_tli(response["signals"])];


def move_according_to_glosa(vehicle):
    '''Moves a vehicle to the predicted glosa'''
    if helper.vehicle_did_not_cross_intersection(vehicle):
        if glosa_exists(vehicle):
            tli_store.remove(vehicle)
        else: 
            visualizer.create_glosa_polyline(vehicle)
        x, y = traci.vehicle.getPosition(vehicle)
        long, lat = traci.simulation.convertGeo(x, y)
        angle = traci.vehicle.getAngle(vehicle)

        glosa, distance, signals = glosa_for_position(lat, long, angle, 30)

        if glosa == None or distance == None or signals == None:
            return 
        
        speed = get_recommended_speed(glosa)
        decision = get_justification(glosa)
        min_speed = get_minimum_speed(glosa)
        max_speed = get_maximum_speed(glosa)
        tli_store.write(traci.simulation.getTime(), vehicle, distance, glosa, signals)

        if not any(x[0] == vehicle for x in influenced_vehicles): 
            print("###### GLOSA for vehicle " + vehicle + " ######")
            print("Calculated speed: " + str(speed) + " km/h with recommendation: " + decision)
            traci.vehicle.setSpeed(vehicle, speed / 3.6)
        else: 
            for v in influenced_vehicles:
                if v[0] == vehicle:
                    if v[2] < min_speed or v[2] * 3.6 > max_speed:
                        traci.vehicle.setSpeed(vehicle, speed / 3.6)
                    break

    else:
        traci.vehicle.setSpeed(vehicle, -1) # give vehicle controls back to simulation if vehicle crossed intersection
    
