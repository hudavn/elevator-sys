from logging import lastResort
import unittest
import threading 
from elevator.Cabinet import Cabinet
from elevator.GlobalState import State

class CabinetTest(unittest.TestCase):
    def test_add_destination(self):
        cabinet = Cabinet(1, 40)
        cabinet.currentFloor = 3
        cabinet.setState(State.MOVEUP)
        cabinet.addDestination(10)
        cabinet.addDestination(10)
        cabinet.addDestination(12)
        cabinet.addDestination(1)
        cabinet.addDestination(3)
        cabinet.addDestination(10)

        self.assertEqual(cabinet.destination, {10, 12})


    def test_check_arrived(self):
        cabinet = Cabinet(1, 40)
        cabinet.setState(State.MOVEUP)
        cabinet.addDestination(10)
        cabinet.addDestination(12)
        cabinet.addDestination(15)

        cabinet.currentFloor = 10
        cabinet.checkArrived()
        self.assertEqual(cabinet.destination, {12, 15})
        self.assertEqual(cabinet.state, State.MOVEUP)

        cabinet.currentFloor = 12
        cabinet.checkArrived()
        self.assertEqual(cabinet.destination, {15})
        self.assertEqual(cabinet.state, State.MOVEUP)

        cabinet.currentFloor = 15
        cabinet.checkArrived()
        self.assertEqual(cabinet.destination, set())
        self.assertEqual(cabinet.state, State.ACTIVE)


    def test_serve_moveup(self):
        cabinet = Cabinet(1, 40)
        cabinet.currentFloor = 8
        cabinet.setState(State.MOVEUP)
        cabinet.addDestination(10)
        threading.Thread(target=cabinet.serve).start()
        self.assertEqual(cabinet.addDestination(cabinet.getPosition()-1), False)
        cabinet.addDestination(20)

        lastState = 8
        while cabinet.state != State.ACTIVE:
            self.assertLessEqual(lastState, cabinet.getPosition())

        self.assertEqual(cabinet.currentFloor, 20)
        self.assertEqual(cabinet.destination, set())


    def test_serve_movedown(self):
        cabinet = Cabinet(1, 40)
        cabinet.currentFloor = 32
        cabinet.setState(State.MOVEDOWN)
        cabinet.addDestination(30)
        threading.Thread(target=cabinet.serve).start()
        self.assertEqual(cabinet.addDestination(cabinet.getPosition()+1), False)
        cabinet.addDestination(20)

        lastState = 32
        while cabinet.state != State.ACTIVE:
            self.assertGreaterEqual(lastState, cabinet.getPosition())

        self.assertEqual(cabinet.currentFloor, 20)
        self.assertEqual(cabinet.destination, set())