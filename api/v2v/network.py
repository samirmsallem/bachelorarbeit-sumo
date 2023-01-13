import traci
from api.sim import helper


def detect_vehicles_waiting_for_turn():
    '''
    Detect vehicles that are waiting to perform a left turn at an intersection but are blocked by forthcoming traffic
    The goal is that if a vehicle fitting this description exists, to find a super vehicle on the forthcoming traffic side, that could prioritize this vehicle by letting it pass (giving way to the oncoming traffic)
    This should have the effect of a better traffic flow.
    preconditions: vehicle's speed is 0, vehicle is somewhere around the stop line, vehicle has no vehicles in front of it, tli is green
    consequences: only vehicles waiting at an intersection will be returned
    returns: [waiting vehicle id, super vehicle to adress]
    '''
    vehicle_ids = traci.vehicle.getIDList()

    for vehicle in vehicle_ids:
        if traci.vehicle.getRoute(vehicle) == traci.route.getEdges("approach3_left") and traci.vehicle.getWaitingTime(vehicle) > 0:
            oncoming_traffic = traci.edge.getLastStepVehicleIDs('approach_2')
            current_lane = traci.vehicle.getLaneID(vehicle)
            length = traci.lane.getLength(current_lane)
            travelled = traci.vehicle.getLanePosition(vehicle)
            if length - 10 < travelled:
                for oncoming_vehicle in oncoming_traffic:
                    if helper.is_super_vehicle(oncoming_vehicle):
                        return [vehicle, oncoming_vehicle]
    
    return [None, None]


def detect_slowed_down_vehicles():
    '''
    Detect vehicles that are slowed down by leading super vehicles
    preconditions: vehicle's speed is bigger than 0, vehicle did not cross intersection yet
    consequences: only vehicles waiting at an intersection will be returned
    returns: a list of [[slowed_down_vehicle_id, perpetrator]]
    '''
    vehicle_ids = traci.vehicle.getIDList()
    slowed_down_vehicles = []

    for vehicle in vehicle_ids:
        if traci.vehicle.getSpeed(vehicle) < 40 / 3.6:
            super_vehicles_infront = find_approaching_in_front_vehicles(vehicle)
            if super_vehicles_infront != None:
                for sup in super_vehicles_infront:
                    slowed_down_vehicles.append([vehicle, sup])

    return slowed_down_vehicles


def detect_waiting_vehicles():
    '''
    Detect vehicles that are waiting at an intersection approach
    preconditions: vehicle's speed is 0, vehicle did not cross intersection yet
    consequences: only vehicles waiting at an intersection will be returned
    '''
    vehicle_ids = traci.vehicle.getIDList()
    waiting_vehicles = []

    for vehicle in vehicle_ids:
        if traci.vehicle.getWaitingTime(vehicle) > 0 and helper.vehicle_did_not_cross_intersection(vehicle): # if vehicle waited (stand still) and did not cross intersection yet
            waiting_vehicles.append(vehicle)

    return waiting_vehicles


def find_approaching_behind_vehicles(vehicle):
    '''
    Detect super vehicles that are approaching an intersection behind a given vehicle
    preconditions: vehicles drive same route as provided vehicle, vehicles are moving, vehicles have driven less distance than provided vehicle (to ensure they are actually behind it)
    consequences: only vehicles driving the same route as provided vehicle will be returned
    '''
    road_id = traci.vehicle.getRoadID(vehicle) # road the vehicle is currently on
    route = traci.vehicle.getRoute(vehicle) # route of the vehicle
    vehicle_pos = traci.vehicle.getLanePosition(vehicle) # distance the vehicle passed on the current road

    current_road_index = route.index(road_id) # index of the road the vehicle is currently on
    i = 0

    approaching_behind_vehicles = []

    while i <= current_road_index: # iterate through all roads until current road, to find all vehicles behind
        
        vehicles_on_edge = traci.edge.getLastStepVehicleIDs(route[i]) # get vehicles on specified road
        if(i == current_road_index): # checking the road where the vehicle is also on
            for vid in vehicles_on_edge:
                if vid == vehicle:
                    continue # ignore own identity 
                approaching_vehicle_pos = traci.vehicle.getLanePosition(vid)
                if helper.is_super_vehicle(vid) and traci.vehicle.getSpeed(vid) > 0 and approaching_vehicle_pos < vehicle_pos and traci.vehicle.getRoute(vid) == route: # if vehicle speed > 0 and vehicle has driven less than sender vehicle and vehicles are driving same route, then add it to the list of receivers
                    approaching_behind_vehicles.append(vid)
            break
        else: # checking previous roads the vehicle already passed
            for vid in vehicles_on_edge:
                if(helper.is_super_vehicle(vid) and traci.vehicle.getRoute(vid) == route): # add vehicle if its driving same direction as requester vehicle
                    approaching_behind_vehicles.append(vid)
            i += 1

    return approaching_behind_vehicles



def find_approaching_in_front_vehicles(vehicle):
    '''
    Detect super vehicles that are approaching an intersection in front of a given vehicle
    preconditions: vehicles drive same route as provided vehicle, vehicles are moving, vehicles have more distance than provided vehicle but did not cross the intersection yet
    consequences: only vehicles driving the same route as provided vehicle will be returned
    '''
    road_id = traci.vehicle.getRoadID(vehicle) # road the vehicle is currently on
    route = traci.vehicle.getRoute(vehicle) # route of the vehicle
    vehicle_pos = traci.vehicle.getLanePosition(vehicle) # distance the vehicle passed on the current road

    current_road_index = helper.get_route_road_index(route, road_id) # index of the road the vehicle is currently on
    approach_index = helper.get_approach_road_index(route) # index of the intersection approach
    i = current_road_index

    approaching_front_vehicles = []

    while i <= approach_index: 
        
        vehicles_on_edge = traci.edge.getLastStepVehicleIDs(route[i]) # get vehicles on the current road
        if(i == current_road_index): # if road is the road that the vehicle is currently on
            for vid in vehicles_on_edge:
                if vid == vehicle:
                    continue # skip own identity
                approaching_vehicle_pos = traci.vehicle.getLanePosition(vid)
                if helper.is_super_vehicle(vid) and approaching_vehicle_pos > vehicle_pos and traci.vehicle.getRoute(vid) == route: # if vehicle has driven more than requester vehicle -> in front of the vehicle
                    approaching_front_vehicles.append(vid)
            break
        else: # the edge is in front of the vehicle anyways
            for vid in vehicles_on_edge:
                if(helper.is_super_vehicle(vid) and traci.vehicle.getRoute(vid) == route): # check if the vehicle will drive the same route, if yes add it
                    approaching_front_vehicles.append(vid)
            i += 1

    return approaching_front_vehicles
