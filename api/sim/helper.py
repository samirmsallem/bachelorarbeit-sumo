import traci
import re
import math
from api.output import logger


def is_super_vehicle(vehicle):
    '''Check whether the given vehicle is a super vehicle (vehicle equipped with GLOSA)'''
    return vehicle in get_super_vehicles(traci.vehicle.getIDList())


def get_super_vehicles(vehicles):  
    '''Returns list of all active super vehicles (vehicles that should be influenced by glosa and other vehicle information)'''
    super_vehicles = []

    for vehicle in vehicles:
        if vehicle.startswith("v2v2i"):
            super_vehicles.append(vehicle)

    return super_vehicles


def get_route_road_index(vehicle_route, searchstring):
    '''Returns the index (on a route) of the given road'''
    approach_route_index = 0
    
    for i, road in enumerate(vehicle_route): # iterate over route array to find edge matching regex, regex is necessary because this is done for all vehicles driving on approach_1,2,3
        match = re.finditer(searchstring, road)
        for m in match:
            approach_route_index = i # get the index of the intersection approach

    return approach_route_index


def get_approach_road_index(vehicle_route):
    '''Returns the index (on a route) of the approach of the intersection (since the vehicle crosses multiple edges (lanes) it is necessary to determine which one is the approach lane)'''
    pattern = r'^approach_' # regex to find approach edges (edges starting with 'approach_')
    approach_route_index = 0

    for i, road in enumerate(vehicle_route): # iterate over route array to find edge matching regex, regex is necessary because this is done for all vehicles driving on approach_1,2,3
        match = re.finditer(pattern, road)
        for m in match:
            approach_route_index = i # get the index of the intersection approach

    return approach_route_index


def vehicle_did_not_cross_intersection(vehicle): # check whether vehicle crossed intersection to prevent further requests
    '''Returns the index (on a route) of the intersection approach (since the vehicle crosses multiple edges (lanes) it is necessary to determine which one is the approach lane)'''
    vehicle_route = traci.vehicle.getRoute(vehicle) # route of vehicle 
    
    current_index = 0
    approach_route_index = get_approach_road_index(vehicle_route)
            
    try:
        current_index = vehicle_route.index(traci.vehicle.getRoadID(vehicle)) # get current edge vehicle is on
    except ValueError:
        return False
    
    logger.printlog("Vehicle " + vehicle + "current: " + str(current_index) + " approach: " + str(approach_route_index) + " condition: " + str(current_index <= approach_route_index))
    return current_index <= approach_route_index # if current position index is greater than intersection approach index -> vehicle crossed intersection

