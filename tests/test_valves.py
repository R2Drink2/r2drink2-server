import unittest
import json
import time
import r2drink2
from r2drink2.valves import Valves, VALVE_INFO_FILE
import serial


class TestValves(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        with open(VALVE_INFO_FILE, 'r') as f:
            cls.valve_info = json.load(f)

        cls.valves = r2drink2.valves.Valves()
        cls.valves.__enter__()
        pass

    @classmethod
    def teardownClass(cls):
        cls.valves.__exit__(None,None,None)
        pass
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_start_stop(self):
        vs = list(self.valve_info)
        vs.sort()
        for v in vs:
            self.valves.start(v)
            time.sleep(1.0)
        for v in vs:
            self.valves.stop(v)
            time.sleep(1.0)
        

