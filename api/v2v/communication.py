import traci
from api.v2v import network, sis, signals
from api.sim import helper
from api.v2i import glosa

com = sis.SharedInformationSpace()

processed_messages = []

def send_alert_messages():
    '''Alerting subsequent vehicles about own waiting state by providing RED signal from signals.py and geoposition'''
    waiting_vehicles = network.detect_waiting_vehicles()

    if len(waiting_vehicles) > 0:
        for vehicle in waiting_vehicles:
            behind_vehicles = network.find_approaching_behind_vehicles(vehicle)
            if len(behind_vehicles) > 0:
                com.write(traci.simulation.getTime(), vehicle, behind_vehicles, signals.Signal.RED, traci.vehicle.getPosition(vehicle))

def send_speed_up_message():
    '''Ask leading super vehicles to speed up in order to allow subsequent traffic to also pass intersection in time'''
    slowed_down_vehicles = network.detect_slowed_down_vehicles()

    if len(slowed_down_vehicles) > 0:
        for entry in slowed_down_vehicles:
            com.write(traci.simulation.getTime(), entry[0], entry[1], signals.Signal.MOVE, traci.vehicle.getPosition(entry[0]))


def send_giving_way_request_message():
    '''Ask oncoming traffic to slow down in order to perform left turn on intersection approach prioritized'''
    waiting_vehicle, counter_part_super_vehicle  = network.detect_vehicles_waiting_for_turn()

    if not (waiting_vehicle == None) and not (counter_part_super_vehicle == None):
        com.write(traci.simulation.getTime(), waiting_vehicle, counter_part_super_vehicle, signals.Signal.TURN, traci.vehicle.getPosition(entry[0]))


def send_messages():
    '''Collection of all possible messages that are sendable, each function call will determine which vehicle should be adressed and will then get notified'''
    send_alert_messages()
    send_speed_up_message()
    send_giving_way_request_message()
    


def collect_messages():
    '''
    Reads all messages inside the Shared Information Space and handle the signals according to their function
    
    Each signal has its own functionality that will get checked and then executed
    '''
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
                    elif message[3] == signals.Signal.MOVE:
                        if not any(entry[2] == signals.Signal.RED and entry[1] == vid for entry in processed_messages):
                            print(f"Enforcing signal {message[3]}: {message[1]} on timestep {message[0]}")
                            new_speed = glosa.get_maximum_speed(glosa.tli_store.read(vid))
                            print(f"{vid}: Speeding up to {new_speed} km/h to allow behind vehicles to cross intersection.")
                            traci.vehicle.setSpeed(vid, new_speed / 3.6)
                    elif message[3] == signals.Signal.TURN:
                        print(f"Enforcing signal {message[3]}: {message[1]} on timestep {message[0]}")
                    
                    processed_messages.append([vid, message[1], message[3]])