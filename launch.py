import os
import sys


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("'SUMO_HOME' var not defined")


from sumolib import checkBinary 
import traci
from api.tli import traffic_light as traffic_light_manager


def run():
    step = 0 # step in simulation count
    ttc = 0 # time to change (traffic light event)
    while traci.simulation.getMinExpectedNumber() > 0:
        if(ttc <= 0): # if next event is ocurring it should get new phases
            new_phases = traffic_light_manager.get_current_phases()
            traci.trafficlight.setRedYellowGreenState('tli', new_phases[0])
            ttc = new_phases[1]
        print("Next traffic signal event in " + str(ttc) + "seconds.")
        traci.simulationStep()
        step += 1
        ttc -= 1
    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "config/osm.sumocfg"])
    run()