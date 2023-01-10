from api.sim import visualizer

class TrafficLightInformation:
    def __init__(self):
        self.informations = []


    def read(self, receiver):
        for tli_info in self.informations:
            if tli_info[1] == receiver:
                return tli_info
    
    def write(self, time, receiver, distance, glosa, signals):
        old_message = self.read(receiver)
        if old_message != None:
            self.informations.remove(old_message)

        self.informations.append((time, receiver, distance, glosa, signals)) 
        # time of type simulation step; 
        # receiver of type simulation vehicle id; 
        # distance of type decimal;
        # glosa of type glosa json;
        # signals of type List [[bulbColor, timeToChange, confidence]]
        visualizer.create_glosa_polyline(receiver)

