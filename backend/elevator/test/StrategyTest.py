from elevator.Cabinet import Cabinet
from elevator.strategy.StandardStrategy import StandardStrategy
from elevator.GlobalState import State
from elevator.SystemManager import SystemManager

import unittest
from unittest import mock
from unittest.mock import patch, Mock

class StandardStrategyTest(unittest.TestCase):   
    global sm 
    sm = SystemManager(4, 10)

    # All cabinets is free
    #
    def test_found_01(self):
        resp = StandardStrategy((5, State.MOVEUP), sm.listOfCabinets)
        self.assertEqual(resp, sm.listOfCabinets[0])

    # Closet cabinet is chosen
    #
    def test_found_02(self):
        # All cabinets is free and last cabinet is closet
        #
        for i in range(len(sm.listOfCabinets)):
            sm.listOfCabinets[i].setState(State.ACTIVE)
            sm.listOfCabinets[i].currentFloor = sm.numberOfFloors - i

        resp = StandardStrategy((1, State.MOVEUP), sm.listOfCabinets)
        self.assertEqual(resp, sm.listOfCabinets[-1])

        # Some cabinets is not free and last cabinet is closet but it is not ACTIVE
        #
        for i in range(len(sm.listOfCabinets)):
            sm.listOfCabinets[i].setState(State.MOVEDOWN if i%2 else State.ACTIVE)
            sm.listOfCabinets[i].currentFloor = sm.numberOfFloors - i

        resp = StandardStrategy((1, State.MOVEDOWN), sm.listOfCabinets)
        self.assertEqual(resp, sm.listOfCabinets[-2])

        # Exist cabinet with the same direction at current requested floor
        #
        sm.listOfCabinets[1].setState(State.MOVEUP)
        sm.listOfCabinets[1].destination.add(7)
        sm.listOfCabinets[1].currentFloor = 7

        resp = StandardStrategy((7, State.MOVEUP), sm.listOfCabinets)
        self.assertEqual(resp, sm.listOfCabinets[1])

    # All cabinets is busy
    #
    def test_not_found_01(self):
        for i in range(len(sm.listOfCabinets)):
            sm.listOfCabinets[i].setState(State.INACTIVE)
        resp = StandardStrategy((0, State.MOVEUP), sm.listOfCabinets)
        self.assertEqual(resp, None)

    # Request with different direction
    #
    def test_not_found_02(self):
        for i in range(len(sm.listOfCabinets)):
            sm.listOfCabinets[i].setState(State.MOVEUP)

        resp = StandardStrategy((5, State.MOVEDOWN), sm.listOfCabinets)
        self.assertEqual(resp, None)

        resp = StandardStrategy((1, State.MOVEDOWN), sm.listOfCabinets)
        self.assertEqual(resp, None)

    # Request with same direction but far away from current level of cabinets
    #
    def test_not_found_03(self):
        for i in range(len(sm.listOfCabinets)):
            sm.listOfCabinets[i].setState(State.MOVEUP)
            sm.listOfCabinets[i].currentFloor = 10

        resp = StandardStrategy((5, State.MOVEUP), sm.listOfCabinets)
        self.assertEqual(resp, None)

        

