import traci
from api.v2v import network
from api.v2v import sis

com = sis.SharedInformationSpace()


def send_messages():
    vehicles = network.detect_waiting_vehicles()

    if(len(vehicles) > 0):
        for vehicle in vehicles:
            behind_vehicles = network.find_approaching_behind_vehicles(vehicle)
            if(len(behind_vehicles) > 0):
                com.write(traci.simulation.getTime(), vehicle, behind_vehicles, 'Waiting at intersection', traci.vehicle.getPosition(vehicle))


def collect_messages():
    vehicle_ids = traci.vehicle.getIDList()
    
    for vid in vehicle_ids:
        messages = com.read(vid)
        if(len(messages) > 0):
            for message in messages:
                print(f"{message[2]}: {message[1]} wrote at {message[0]}: {message[3]}")