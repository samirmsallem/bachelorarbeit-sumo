import traci
import sys
import threading
from api.v2i import traffic_light as traffic_light_manager
from api.v2i import glosa as glosa_manager
from api.v2v import communication as v2v_client
from api.output import logger,plotter
from api.sim import helper
from api.sim import visualizer


plot_data = []


def run_sim():
    '''Main function that performs simulation steps and executes the v2i and v2v logic'''
    thread = threading.Thread(target=plotter.plot_speed)
    thread.start()

    step = 0 # step in simulation count
    ttc = 0 # time to change (traffic light event)
    while traci.simulation.getMinExpectedNumber() > 0:
        visualizer.clear_all_polylines()
        vehicles = traci.vehicle.getIDList()
        v2v_client.send_messages()
        v2v_client.collect_messages()

        if(ttc <= 0): # handle traffic lights at intersection
            state, ttc = traffic_light_manager.get_current_phases()
            traci.trafficlight.setRedYellowGreenState('tli', state)

        if(step > 0 and step % 3 == 0): # handle vehicles following green light optimal speed advisory (glosa)
            for vehicle in helper.get_super_vehicles(vehicles):
                glosa_manager.move_according_to_glosa(vehicle)

        if(step > 0 and 'v2v2i.0' in vehicles):
            plot_data.append(traci.vehicle.getSpeed('v2v2i.0'))
            plotter.plot_queue.put(plot_data[:])  # add the data to the queue

        logger.printlog("Next traffic signal event in " + str(ttc) + "seconds.")       

        traci.simulationStep()

        step += 1
        ttc -= 1

    traci.close()
    sys.stdout.flush()


def start_simulation(sumo_binary, sumo_config_file):
    '''Starts the Sumo simulation using the provided sumo config file in TraCI'''
    traci.start([sumo_binary, "-c", sumo_config_file])
    run_sim()
