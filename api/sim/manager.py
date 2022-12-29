from sumolib import checkBinary 
import traci
import re
import sys
from api.tli import traffic_light as traffic_light_manager
from api.tli import glosa as glosa_manager
from api.output import logger


def get_super_vehicles(): # returns list of all active super vehicles (vehicles that should be influenced by glosa and other vehicle information)
  super_vehicles = []

  for vehicle in traci.vehicle.getIDList():
    if vehicle.startswith("super"):
      super_vehicles.append(vehicle)

  return super_vehicles


def run_sim():
    step = 0 # step in simulation count
    ttc = 0 # time to change (traffic light event)
    while traci.simulation.getMinExpectedNumber() > 0:

        if(ttc <= 0): # handle traffic lights at intersection
            state, ttc = traffic_light_manager.get_current_phases()
            traci.trafficlight.setRedYellowGreenState('tli', state)

        if(step > 0 and step % 3 == 0): # handle vehicles following green light optimal speed advisory (glosa)
            for vehicle in get_super_vehicles():
                if(vehicle_did_not_cross_intersection(vehicle)):
                    x, y = traci.vehicle.getPosition(vehicle)
                    lon, lat = traci.simulation.convertGeo(x, y)
                    angle = traci.vehicle.getAngle(vehicle)

                    speed, decision = glosa_manager.glosa_for_position(lat, lon, angle, 30)
                    print("###### Vehicle " + vehicle + " ######")
                    print("Calculated speed: " + str(speed) + " km/h with recommendation: " + decision)
                    traci.vehicle.setSpeed(vehicle, speed / 3.6)
                else:
                    traci.vehicle.setSpeed(vehicle, -1)  

        logger.print("Next traffic signal event in " + str(ttc) + "seconds.")       

        traci.simulationStep()

        step += 1
        ttc -= 1

    traci.close()
    sys.stdout.flush()



def start_simulation(sumo_config_file):
    sumoBinary = checkBinary('sumo-gui')
    traci.start([sumoBinary, "-c", sumo_config_file])
    run_sim()


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