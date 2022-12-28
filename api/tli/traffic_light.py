from api.rest import client
from api.output import logger

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


def pretty_print_tli(phases):
    for phase in phases:
        logger.print(phase[0] + " phase for " + str(phase[1]) + " seconds. Confidence: " + str(phase[2]) + "%")


def get_approach_signal(approachId):
    if approachId == 1:
        logger.print("###### Approach 1 ######")
        return extract_tli(client.perform_request(48.76280618764156, 11.427623411273599, 105.4492514593)["signals"])
    elif approachId == 2:
        logger.print("###### Approach 2 ######")
        return extract_tli(client.perform_request(48.763513657462475, 11.431514833553978, 235.909123032)["signals"])
    else:
        logger.print("###### Approach 3 ######")
        return extract_tli(client.perform_request(48.758733700993886, 11.425519395220782, 40.2685517938)["signals"])


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