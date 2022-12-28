import traci
from api.output import logger
import re

def vehicle_did_not_cross_intersection(vehicle): # check whether vehicle crossed intersection to prevent further requests
    pattern = r'^approach_' # regex to find approach edges
    vehicle_route = traci.vehicle.getRoute(vehicle) # route of vehicle 
    approach_route_index = 0
    current_index = 0

    for i, road in enumerate(vehicle_route): # iterate over route array to find edge matching regex, regex is necessary because this is done for all vehicles driving on approach_1,2,3
        match = re.finditer(pattern, road)
        for m in match:
            approach_route_index = i # get the index of the intersection approach
            
    try:
        current_index = vehicle_route.index(traci.vehicle.getRoadID(vehicle)) # get current edge vehicle is on
    except ValueError:
        return False
    
    logger.print("Vehicle " + vehicle + "current: " + str(current_index) + " approach: " + str(approach_route_index) + " condition: " + str(current_index <= approach_route_index))
    return current_index <= approach_route_index # if current position index is greater than intersection approach index -> vehicle crossed intersection