from pyexpat.errors import messages
from api.sim import visualizer

class SharedInformationSpace:
    def __init__(self):
        self.messages = []
    
    def write(self, time, sender, receivers, signal, data):
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
        messages = []
        for message in self.messages:
            if message[2] == receiver:
                messages.append(message)
        return messages

