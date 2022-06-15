from collections import OrderedDict
from datetime import datetime
import threading
from time import sleep

from elevator.Cabinet import Cabinet
from elevator.GlobalState import State 
from elevator.strategy.StandardStrategy import StandardStrategy
import secrets

class SystemManager:
    def __init__(self, numberOfCabinets, numberOfFloors):
        if numberOfCabinets < 1: 
            raise Exception("System must have at least 1 cabinet")
        if numberOfFloors < 1:
            raise Exception("Building must have at least 1 floor to use this system")

        self.numberOfCabinets = numberOfCabinets
        self.numberOfFloors = numberOfFloors
        self.listOfCabinets= [Cabinet(i, self.numberOfFloors) for i in range(self.numberOfCabinets)]
        self.requestQueue = []
        self.serveIndex = 0
        self.servant = {}
        self.status = State.INACTIVE
        self.lock = threading.Lock()

    def on(self): self.status = State.ACTIVE
    def off(self): self.status = State.INACTIVE
    def onCabinet(self, index): self.listOfCabinets[index].setState(State.ACTIVE)
    def offCabinet(self, index): self.listOfCabinets[index].setState(State.INACTIVE)
    def A(self): self.lock.acquire()
    def R(self): self.lock.release()

    def getServant(self, serveIndex): return self.servant[serveIndex][1]

    def getStatus(self, index = None):
        self.A()
        resp = OrderedDict()
        if index == None:
            resp["model"] =  "Campus Elevator System"
            resp["version"] = "v1.0.2"
            resp["builder"] = "datnh2"
            resp["owner"] = "VNG Campus"
            resp["timestamp"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            resp["status"] = self.status.name
            resp["cabinets"] = self.numberOfCabinets
            resp["floors"] = self.numberOfFloors

            queue = []
            detail = []
            for i in range(len(self.requestQueue)):
                info = OrderedDict()
                info['index'] = self.requestQueue[i][1][0]
                info['floor'] = self.requestQueue[i][1][1]
                info['action'] = self.requestQueue[i][1][2].name
                queue.append(info)

            for i in range(len(self.listOfCabinets)):
                info = OrderedDict()
                info['index'] = self.listOfCabinets[i].index
                info['floor'] = self.listOfCabinets[i].currentFloor
                info['status'] = self.listOfCabinets[i].state.name
                info['destinationCount'] = len(self.listOfCabinets[i].destination)
                detail.append(info)
            
            resp['requests'] =len(queue)
            resp['queue'] = queue
            resp['detail'] = detail
        else:
            resp['index'] = self.listOfCabinets[index].index
            resp['floor'] = self.listOfCabinets[index].currentFloor
            resp['status'] = self.listOfCabinets[index].state.name
            resp['destinationCount'] = len(self.listOfCabinets[index].destination)
            resp['destination'] = list(self.listOfCabinets[index].destination)

        self.R()
        return resp


    def request(self, direction, floor): 
        if direction not in [0, 1]:
            raise Exception("Illegal direction argument passed")
        elif floor < 1 or floor > self.numberOfFloors: 
            raise Exception("Illegal floor argument passed")
        
        if self.status == State.INACTIVE:
            return -1
        else:
            self.A()
            self.serveIndex += 1
            self.servant.update({self.serveIndex: (secrets.token_hex(16), None)})
            self.requestQueue.append((0, (self.serveIndex, floor, State.MOVEUP if direction else State.MOVEDOWN)))
            self.R()
            return (self.serveIndex, self.servant[self.serveIndex][0])


    def cabinRequest(self, servant, floor):
        if floor < 1 or floor > self.numberOfFloors: 
            raise Exception("Illegal floor argument passed")

        ok = servant.addDestination(floor)
        if ok and servant.state == State.ACTIVE:
            self.requestQueue.append((1, servant, floor))

        return ok


    def serve(self):
        while self.status == State.ACTIVE:
            if len(self.requestQueue):
                if self.requestQueue[0][0] == 0:
                    choosenCabinet = StandardStrategy((self.requestQueue[0][1][1], self.requestQueue[0][1][2]), self.listOfCabinets)
                    if choosenCabinet: 
                        request = self.requestQueue.pop(0)[1]
                        if choosenCabinet.getPosition() != request[1]:
                            choosenCabinet.addDestination(request[1])
                            self.servant.update({request[0]: (self.servant[request[0]][0], choosenCabinet)})

                            if choosenCabinet.state == State.ACTIVE:
                                choosenCabinet.firstPick = request[1]
                                choosenCabinet.setState(request[2])
                                threading.Thread(target=choosenCabinet.serve).start()
                else: 
                    request = self.requestQueue.pop(0)
                    choosenCabinet = request[1]
                    floor = request[2]
                    if choosenCabinet.state == State.ACTIVE:
                        if choosenCabinet.getPosition() < floor:
                            choosenCabinet.setState(State.MOVEUP)
                        elif choosenCabinet.getPosition() > floor:
                            choosenCabinet.setState(State.MOVEDOWN)
                        threading.Thread(target=choosenCabinet.serve).start()
        



