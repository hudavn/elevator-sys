from cabinetState import State

class Cabinet: 
    def __init__(self, upper_bound):
        if upper_bound < 1: 
            raise Exception("It must be worked in building with at least 1 floor.")

        self.upper_bound = upper_bound
        self.lower_bound = 0
        self.currentFloor = 1
        self.state = State.FREE.name

    def getPosition(self): return self.currentFloor
    def isFree(self): return self.state == State.FREE.name
    
    def setState(self, state): self.state = state

    def moveUp(self): 
        if self.currentFloor == self.upper_bound: return False
        self.currentFloor += 1
        return True

    def moveDown(self):
        if self.currentFloor == self.lower_bound: return False
        self.currentFloor -= 1
        return True