from concurrent.futures import thread
from random import randint
import unittest
import json
import threading
import time

from elevator.GlobalState import State
from elevator.SystemManager import SystemManager


class SystemManagerTest(unittest.TestCase):
    def test_turn_on(self):
        sm = SystemManager(4, 40)
        self.assertEqual(sm.status, State.INACTIVE)
        sm.on()
        self.assertEqual(sm.status, State.ACTIVE)

    def test_get_status(self):
        sm = SystemManager(4, 40)
        with open("test_get_status_01.json", "w") as f:
            f.write(json.dumps(sm.getStatus(), indent=4))

        sm.on()
        sm.request(0, 10)
        sm.request(1, 2)
        sm.request(1, 30)
        for i in range(sm.numberOfCabinets):
            sm.listOfCabinets[i].currentFloor = randint(1, sm.numberOfFloors)
            sm.listOfCabinets[i].setState(State.INACTIVE if i%2 else State.ACTIVE)

        with open("test_get_status_02.json", "w") as f:
            f.write(json.dumps(sm.getStatus(), indent=4))

    def test_serve_01(self):
        sm = SystemManager(2, 40)
        sm.on()
        threading.Thread(target=sm.serve).start()
        sm.request(0, 10)
        sm.request(1, 2)
        sm.request(1, 30)
        sm.request(0, 28)
        time.sleep(3)
        sm.request(1, 1)

        while len(sm.requestQueue):
            continue

        sm.off()



