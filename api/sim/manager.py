import traci
import sys
import threading
from api.v2i import traffic_light as traffic_light_manager
from api.v2i import glosa as glosa_manager
from api.output import logger,plotter
from api.sim import helper


plot_data = []

def move_according_to_glosa(vehicle):
    if(helper.vehicle_did_not_cross_intersection(vehicle)):
        x, y = traci.vehicle.getPosition(vehicle)
        lon, lat = traci.simulation.convertGeo(x, y)
        angle = traci.vehicle.getAngle(vehicle)

        speed, decision = glosa_manager.glosa_for_position(lat, lon, angle, 30)
        logger.printlog("###### Vehicle " + vehicle + " ######")
        logger.printlog("Calculated speed: " + str(speed) + " km/h with recommendation: " + decision)
        traci.vehicle.setSpeed(vehicle, speed / 3.6)
    else:
        traci.vehicle.setSpeed(vehicle, -1)


def run_sim():

    thread = threading.Thread(target=plotter.plot_speed)
    thread.start()

    step = 0 # step in simulation count
    ttc = 0 # time to change (traffic light event)
    while traci.simulation.getMinExpectedNumber() > 0:

        if(ttc <= 0): # handle traffic lights at intersection
            state, ttc = traffic_light_manager.get_current_phases()
            traci.trafficlight.setRedYellowGreenState('tli', state)

        if(step > 0 and step % 3 == 0): # handle vehicles following green light optimal speed advisory (glosa)
            for vehicle in helper.get_super_vehicles():
                move_according_to_glosa(vehicle)

        if(step > 0):
            plot_data.append(traci.vehicle.getSpeed('super1'))
            plotter.plot_queue.put(plot_data[:])  # add the data to the queue   

        logger.printlog("Next traffic signal event in " + str(ttc) + "seconds.")       

        traci.simulationStep()

        step += 1
        ttc -= 1

    traci.close()
    sys.stdout.flush()



def start_simulation(sumo_binary, sumo_config_file):
    traci.start([sumo_binary, "-c", sumo_config_file])
    run_sim()
