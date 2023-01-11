import traci
from api.v2v import network, sis, signals
from api.sim import helper
from api.v2i import glosa

com = sis.SharedInformationSpace()

processed_messages = []

'''
Alerting subsequent vehicles about own waiting state by providing RED signal from signals.py and geoposition
'''
def send_alert_messages():
    waiting_vehicles = network.detect_waiting_vehicles()

    if(len(waiting_vehicles) > 0):
        for vehicle in waiting_vehicles:
            behind_vehicles = network.find_approaching_behind_vehicles(vehicle)
            if(len(behind_vehicles) > 0):
                com.write(traci.simulation.getTime(), vehicle, behind_vehicles, signals.Signal.RED, traci.vehicle.getPosition(vehicle))


def send_messages():
    send_alert_messages()
    


def collect_messages():
    vehicle_ids = traci.vehicle.getIDList()
    
    for vid in vehicle_ids:
        messages = com.read(vid)
        if(len(messages) > 0):
            for message in messages:
                if not any(signal[0] == vid and signal[1] == message[1] and signal[2] == message[3] for signal in processed_messages):
                    if message[3] == signals.Signal.RED:
                        if helper.is_super_vehicle(vid):
                            if not glosa.glosa_exists(vid):
                                com.messages.remove(message)
                                continue
                            print(f"Enforcing signal {message[3]}: {message[1]} on timestep {message[0]} at position {message[4]}")
                            x, y = message[4]
                            ttg = glosa.improve_vehicle_speed(vid, traci.vehicle.getDrivingDistance2D(vid, x, y))
                            com.write(traci.simulation.getTime(), vid, [message[1]], signals.Signal.TTG, ttg)
                    elif message[3] == signals.Signal.TTG:
                        print(f"Enforcing signal {message[3]}: {message[1]} on timestep {message[0]} with time-to-green: {message[4]}")
                    
                    processed_messages.append([vid, message[1], message[3]])