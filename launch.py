from api.sim import manager as simulation_manager
import os
import sys


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("'SUMO_HOME' var not defined")

if __name__ == "__main__":
    simulation_manager.start_simulation("config/osm.sumocfg")