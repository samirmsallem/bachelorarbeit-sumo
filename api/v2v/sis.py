import threading
from api.sim import visualizer

class SharedInformationSpace:
    def __init__(self):
        self.messages = []
        self.lock = threading.Lock()
    
    def write(self, time, sender, receivers, message):
        with self.lock:
            for receiver in receivers:
                self.messages.append((time, sender, receiver, message))
                visualizer.create_vehicle_polyline(sender, receiver)
    
    def read(self, receiver):
        with self.lock:
            messages = []
            for message in self.messages:
                if message[2] == receiver:
                    messages.append(message)
                    self.messages.remove(message)
            return messages

