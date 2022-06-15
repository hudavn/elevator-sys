from locale import currency
from elevator.GlobalState import State

def StandardStrategy(request, cabinets):
    currentFloor, direction = request

    distance = 200
    result = None

    for cabinet in cabinets:
        if (cabinet.state == direction and currentFloor in cabinet.destination):
            return cabinet
            
        elif cabinet.state == State.ACTIVE or \
            (cabinet.getPosition() >= currentFloor and cabinet.state == State.MOVEDOWN == direction) or \
            (cabinet.getPosition() <= currentFloor and cabinet.state == State.MOVEUP == direction):
                if  result == None or \
                    (result.state == cabinet.state and distance > abs(cabinet.getPosition() - currentFloor)) or \
                    (result.state != State.ACTIVE and cabinet.state == State.ACTIVE):
                        distance = abs(cabinet.getPosition() - currentFloor)
                        result = cabinet

    return result
