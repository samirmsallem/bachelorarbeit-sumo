class TrafficLightInformation:
    def __init__(self):
        self.informations = []


    def read(self, receiver):
        '''
        Returns the TLI entry received for the provided receiver (vehicle)
        The entry contains of:
        - the timestamp the information was stored, 
        - the receiver of the message (must be equal to the caller of this function)
        - the distance to the intersection stopline
        - the glosa prediction for the vehicle
        - a list of upcoming signals (phases, [[bulbColor, timeToChange, confidence]] )
        '''
        for tli_info in self.informations:
            if tli_info[1] == receiver:
                return tli_info

    def remove(self, receiver):
        '''Removes the TLI entry of a given vehicle (receiver)'''
        for tli_info in self.informations:
            if tli_info[1] == receiver:
                self.informations.remove(tli_info)
    
    def write(self, time, receiver, distance, glosa, signals):
        '''Writes the received data through v2i communication into the TLI storage'''
        old_message = self.read(receiver)
        if old_message != None:
            self.informations.remove(old_message)

        self.informations.append((time, receiver, distance, glosa, signals)) 
        # time of type simulation step; 
        # receiver of type simulation vehicle id; 
        # distance of type decimal;
        # glosa of type glosa json;
        # signals of type List [[bulbColor, timeToChange, confidence]]

