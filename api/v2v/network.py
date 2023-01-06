import traci
from api.sim import helper

'''
detect vehicles that are waiting at an intersection approach
preconditions: vehicle's speed is 0, vehicle did not cross intersection yet
consequences: only vehicles waiting at an intersection will be returned
'''
def detect_waiting_vehicles():
    vehicle_ids = traci.vehicle.getIDList()
    waiting_vehicles = []

    for vehicle in vehicle_ids:
        if traci.vehicle.getWaitingTime(vehicle) > 0 and helper.vehicle_did_not_cross_intersection(vehicle): # if vehicle waited (stand still) and did not cross intersection yet
            waiting_vehicles.append(vehicle)

    return waiting_vehicles


'''
detect vehicles that are approaching an intersection behind a given vehicle
preconditions: vehicles drive same route as provided vehicle, vehicles are moving, vehicles have driven less distance than provided vehicle (to ensure they are actually behind it)
consequences: only vehicles driving the same route as provided vehicle will be returned
'''
def find_approaching_behind_vehicles(vehicle):
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
                if traci.vehicle.getSpeed(vid) > 0 and approaching_vehicle_pos < vehicle_pos and traci.vehicle.getRoute(vid) == route: # if vehicle speed > 0 and vehicle has driven less than sender vehicle and vehicles are driving same route, then add it to the list of receivers
                    approaching_behind_vehicles.append(vid)
            break
        else: # checking previous roads the vehicle already passed
            for vid in vehicles_on_edge:
                if(traci.vehicle.getRoute(vid) == route): # add vehicle if its driving same direction as requester vehicle
                    approaching_behind_vehicles.append(vid)
            i += 1

    return approaching_behind_vehicles



def find_approaching_in_front_vehicles(vehicle):
    road_id = traci.vehicle.getRoadID(vehicle) # road the vehicle is currently on
    route = traci.vehicle.getRoute(vehicle) # route of the vehicle
    vehicle_pos = traci.vehicle.getLanePosition(vehicle) # distance the vehicle passed on the current road

    current_road_index = route.index(road_id) # index of the road the vehicle is currently on
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
                if approaching_vehicle_pos > vehicle_pos and traci.vehicle.getRoute(vid) == route: # if vehicle has driven more than requester vehicle -> in front of the vehicle
                    approaching_front_vehicles.append(vid)
            break
        else: # the edge is in front of the vehicle anyways
            for vid in vehicles_on_edge:
                if(traci.vehicle.getRoute(vid) == route): # check if the vehicle will drive the same route, if yes add it
                    approaching_front_vehicles.append(vid)
            i += 1

    return approaching_front_vehicles
