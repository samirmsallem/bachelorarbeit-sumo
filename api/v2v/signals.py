import enum

# The vehicle will send this signal if..
class Signal(enum.Enum):
    
    RED = 'Waiting at intersection' # it waits at an intersection
    # goal: Vehicles equipped with GLOSA predictions can improve their speed forecast by using these signals.

    MOVE = 'Want to catch green wave' # it is driving behind a vehicle equipped with glosa
    # goal: better traffic flow by allowing more vehicles to pass intersection in time.
    #       e.g: GLOSA vehicle receives a recommendation of at least 30km/h. Normally it would now drive 30 km/h and cross intersection before turning red,
    #       but in order to increase traffic flow it will drive e.g. 40 km/h so that the senders of this command will also be able to cross intersection before turning red

    TURN = 'Waiting for clear lane to turn' # it wants to perform a left/right turn at the intersection but has to wait for the oncoming traffic
    # goal: If oncoming traffic is overloaded, a vehicle will stop in order to allow the sender to make a turn instead of waiting an endless amount of time
    #       This message will be sent to the leading vehicle in the oncoming traffic. Next this vehicle will check whether it is possible to break or if this would 
    #       affect the own traffic flow in a negative way
