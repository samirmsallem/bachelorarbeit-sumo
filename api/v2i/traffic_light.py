from api.rest import client
from api.output import logger


'''
Extract current signal phases from the response json

Exemplary function response: 

[["Green", 11, 97], ["Red", 45, 95]]

-> Indicates that current phase is green and has a duration of 11s. This prediction is made with 97% probability. Next is red phase for 45s with 95% probability.
'''
def extract_tli(signals):
    phases = []
    count = len(signals[0]["predictions"])
    predictions = signals[0]["predictions"]

    if(count == 0):
        return None
    else:
        phases.append([signals[0]["bulbColor"], predictions[0]["timeToChange"], predictions[0]["confidence"]])
        if(count == 2):
            phases.append([predictions[0]["bulbColor"], predictions[1]["timeToChange"] - predictions[0]["timeToChange"], predictions[1]["confidence"]])
        
        pretty_print_tli(phases)
        return phases


'''
Prints the above extracted phases
'''
def pretty_print_tli(phases):
    for phase in phases:
        logger.printlog(phase[0] + " phase for " + str(phase[1]) + " seconds. Confidence: " + str(phase[2]) + "%")


'''
Returns signals for the given approach

Background of this function is that in order to control the traffic signal heads in the simulation like in real-life through the API, 
i need to obtain these signals and then pass them to the simulation handler
Since i cannot just ask the API to provide signals for a given approach at an intersection, i have to request the signals through a point
The points specified in the function calls below stand for a point at each approach which will then return signals for the requested approach
'''
def get_approach_signal(approachId):
    if approachId == 1:
        logger.printlog("###### Approach 1 ######")
        return extract_tli(client.perform_request(48.76280618764156, 11.427623411273599, 105.4492514593)["signals"])
    elif approachId == 2:
        logger.printlog("###### Approach 2 ######")
        return extract_tli(client.perform_request(48.763513657462475, 11.431514833553978, 235.909123032)["signals"])
    else:
        logger.printlog("###### Approach 3 ######")
        return extract_tli(client.perform_request(48.758733700993886, 11.425519395220782, 40.2685517938)["signals"])


'''
Returns all current signals for all approaches and the next signal change time (time to change (ttc))

The SUMO Traffic Light State Manager contains a number of signal heads. 
For the intersection selected for this simulation, there is one signal head for each approach, meaning that i have 3 signal heads to control.
The signal phases are represented in a character list e.g. 'rgg' whereby each character represents the current phase for a signal head. 
In this case the first signal head is described with 'r' (red) whereas the second and third are 'g' (green)

The function below requests the current phase for each approach and the ttc for the upcoming phase.
The smallest ttc (next timestep at which a signal head will change at the intersection) will be stored and returned, so that if the simulation reaches that time, 
a new request will be created.

Furthermore the function parses the json phases into sumo signals (json response "Green" -> sumo 'g' (same goes for 'Red' -> 'r'))

'''
def get_current_phases():
    approach2 = get_approach_signal(2) # first argument in sumo traffic light phase definition
    approach3 = get_approach_signal(3) # second argument
    approach1 = get_approach_signal(1) # third argument

    if(approach2 == None or approach3 == None or approach1 == None):
        return get_current_phases()

    ttc = min([approach2[0][1], approach3[0][1], approach1[0][1]])

    currentphase = ''

    for phase in [approach2, approach3, approach1]:
        if(phase[0][0] == 'Green'):
            currentphase += 'g'
        else:
            currentphase += 'r'
    
    return [currentphase, ttc]


def main():
    get_approach_signal(1)
    get_approach_signal(2)
    get_approach_signal(3)


if __name__ == "__main__":
    main()