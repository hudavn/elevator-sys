from stat import filemode
from elevator.GlobalState import State
import time
import threading
import logging

class Cabinet: 
    def __init__(self, index, upper_bound):
        if upper_bound < 1: 
            raise Exception("It must be worked in building with at least 1 floor.")

        self.upper_bound = upper_bound
        self.lower_bound = 0
        self.currentFloor = 1
        self.state = State.ACTIVE
        self.destination = set()
        self.index = index
        self.firstPick = None
        self.lock = threading.Lock()

    def getPosition(self): return self.currentFloor
    def A(self): self.lock.acquire()
    def R(self): self.lock.release()
    def setState(self, state): self.state = state

    def removeDestination(self, floor): 
        if floor in self.destination: 
            self.A()
            self.destination.remove(floor)
            self.R()
            return True
        return False

    def addDestination(self, floor): 
        self.A()
        if self.currentFloor == floor: 
            self.R()
            return True
        if (self.currentFloor < floor and self.state == State.MOVEUP) or \
            (self.currentFloor > floor and self.state == State.MOVEDOWN) or \
            self.state == State.ACTIVE: 
                self.destination.add(floor) 
                self.R()
                logging.info(f"Cabin [{self.index}]:{self.state.name}: Add new destination: floor [{floor}]")
                return True
        self.R()
        return False

    
    def checkArrived(self): 
        if self.currentFloor in self.destination:
            logging.info(f"Cabin [{self.index}]:{self.state.name}:  Stopping at floor [{self.currentFloor}] for drop/pick passengers")
            time.sleep(5)
            self.removeDestination(self.currentFloor)

            if len(self.destination) == 0:
                self.setState(State.ACTIVE)
                logging.info(f"Cabin [{self.index}] is FREE - Floor [{self.currentFloor}]")

            
    def moveUp(self): 
        if self.currentFloor == self.upper_bound: return False

        self.A()
        self.currentFloor += 1
        time.sleep(1)
        self.R()

        if self.firstPick == None or self.currentFloor == self.firstPick:
            self.checkArrived()

        return True

    def moveDown(self):
        if self.currentFloor == self.lower_bound: return False

        self.A()
        self.currentFloor -= 1
        time.sleep(1)
        self.R()

        if self.firstPick == None or self.currentFloor == self.firstPick:
            self.checkArrived()

        return True

    def serve(self):
        if self.firstPick != None:
            while self.currentFloor != self.firstPick:
                if self.currentFloor < self.firstPick: 
                    self.moveUp()
                else:
                    self.moveDown()

        self.checkArrived() # In case request from current floor
        self.firstPick = None

        while self.state != State.ACTIVE:
            if self.state == State.MOVEDOWN: 
                self.moveDown()
            else: 
                self.moveUp()
