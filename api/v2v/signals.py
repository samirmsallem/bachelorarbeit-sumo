import enum


class Signal(enum.Enum):
    
    RED = 'Waiting at intersection' 
    '''The vehicle will send this signal if it waits at an intersection

           goal: Vehicles equipped with GLOSA predictions can improve their speed forecast by reading these signals.'''

    TTG = 'Time to green' 
    '''The vehicle will send this signal if it is a super vehicle (equipped with glosa information) and received a RED signal from a waiting vehicle

           goal: The vehicle received geo position data of a waiting vehicle, this data can be used in order to improve the glosa algorithm
           To also give the sender vehicle a benefit, with this signal it will receive the TTG (time to green) until the signal turns green again
           this information can be used to give the driver awarness of the upcoming phase.
           This could also be useful if the vehicle is an autonoumus vehicle since it does not need to look at the signal head itself, if it knows when the traffic signal turns green'''
    
    MOVE = 'Want to catch green wave' 
    '''The vehicle will send this signal if it is driving behind a vehicle equipped with glosa

           goal: better traffic flow by allowing more vehicles to pass intersection in time.
           e.g: GLOSA vehicle receives a recommendation of at least 30km/h. Normally it would now drive 30 km/h and cross intersection before turning red,
           but in order to increase traffic flow it will drive e.g. 40 km/h so that the senders of this command will also be able to cross intersection before turning red'''

    TURN = 'Waiting for clear lane to turn' 
    '''The vehicle will send this signal if it wants to perform a left/right turn at the intersection but has to wait for the oncoming traffic

           goal: If oncoming traffic is overloaded, a vehicle will stop in order to allow the sender to make a turn instead of waiting an endless amount of time
           This message will be sent to the leading vehicle in the oncoming traffic. Next this vehicle will check whether it is possible to break or if this would 
           affect the own traffic flow in a negative way'''
