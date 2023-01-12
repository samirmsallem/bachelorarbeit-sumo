import traci


def clear_all_polylines():
    '''Clears all polylines of the type 'v2v' and 'v2i' (communication polylines)'''
    for polyline in traci.polygon.getIDList():
        if(traci.polygon.getType(polyline) in ['v2v', 'v2i']):
            traci.polygon.remove(polyline)


def create_vehicle_polyline(v1, v2):
    '''Creates a communication polyline between v1 -> v2 (v2v communication), if v1 is a super vehicle the polyline will be light green, otherwise white'''
    if all(v in traci.vehicle.getIDList() for v in [v1, v2]):
        pos1 = traci.vehicle.getPosition(v1)
        pos2 = traci.vehicle.getPosition(v2)

        traci.polygon.add('com_' + v1 + '_' + v2, [pos1, pos2], (124, 252, 0, 255) if v1.startswith("super") else (255, 255, 255, 255), False, "v2v", 999, 0.1)

def create_glosa_polyline(vehicle):
    '''Creates a communication polyline between v1 -> traffic light, this represents the v2i communication (blue polyline)'''
    pos1 = traci.vehicle.getPosition(vehicle)

    traci.polygon.add('com_' + vehicle + '_intersection', [pos1, [260, 440]], (0, 0, 255, 255), False, "v2i", 999, 0.1)
