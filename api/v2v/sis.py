from pyexpat.errors import messages
from api.sim import visualizer

class SharedInformationSpace:
    def __init__(self):
        self.messages = []
    
    def write(self, time, sender, receivers, signal, data):
        '''Writes the received data through v2i and v2v2i communication into the shared information space'''
        for receiver in receivers:
            if not any(message[1] == sender and message[2] == receiver and message[3] == signal for message in self.messages):
                self.messages.append((time, sender, receiver, signal, data)) 
                # time of type simulation step; 
                # sender of type simulation vehicle id; 
                # receiver of type simulation vehicle id;
                # signal of type signal enum (signals.py)
                # data of type Any (e.g. gps position, speed..)
                visualizer.create_vehicle_polyline(sender, receiver)
    
    def read(self, receiver):
        '''
        Returns all messages inside the shared information space adressed to the receiver (vehicle)
        One entry contains of:
        - the timestamp the information was stored, 
        - the sender of the message (cannot be equal to the receiver)
        - the receiver of the message (must be equal to the provided receiver)
        - a signal of enum type Signal (signals.py)
        - data (position, tli predictions, vehicle amount..)
        '''
        messages = []
        for message in self.messages:
            if message[2] == receiver:
                messages.append(message)
        return messages

