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
from api.tli import glosa as glosa_manager
from api.misc import logger


def run():
    step = 0 # step in simulation count
    ttc = 1 # time to change (traffic light event)
    while traci.simulation.getMinExpectedNumber() > 0:

        if(ttc <= 0): # handle traffic lights at intersection
            state, ttc = traffic_light_manager.get_current_phases()
            traci.trafficlight.setRedYellowGreenState('tli', state)

            for vehicle in ['super1', 'super2', 'super3']:
                x, y = traci.vehicle.getPosition(vehicle)
                lon, lat = traci.simulation.convertGeo(x, y)
                angle = traci.vehicle.getAngle(vehicle)
                currentspeed = traci.vehicle.getSpeed(vehicle) * 3.6

                speed, decision = glosa_manager.glosa_for_position(lat, lon, angle, currentspeed)
                logger.print("###### Vehicle " + vehicle + " ######")
                logger.print("Calculated speed: " + str(speed) + " km/h with recommendation: " + decision)
                traci.vehicle.setSpeed(vehicle, speed / 3.6)

        logger.print("Next traffic signal event in " + str(ttc) + "seconds.")       

        traci.simulationStep()
        step += 1
        ttc -= 1
    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "config/osm.sumocfg"])
    run()