import unittest
import json
import time
import r2drink2.app
from r2drink2.valves import Valves

class MockValves(Valves):
    def _write_serial(self, val):
        print val

class TestApp(unittest.TestCase):
    
    @classmethod
    def setupClass(cls):
        cls.valves = MockValves()
        cls.valves.__enter__()
        pass

    @classmethod
    def teardownClass(cls):
        cls.valves.__exit__(None,None,None)
        pass
    
    def setUp(self):
        self.app = r2drink2.app.APP
        self.app.valves = self.valves
        self.c = self.app.test_client()
    
    def tearDown(self):
        pass

    def test_pour(self):
        ret = self.c.post('/pour',
                          data=json.dumps(
                              {
                                  'qty':3.0,
                                  'ingredients':{
                                      'Malibu Rum':2.0,
                                      'Midori Melon Liqueur':1.0,
                                      'Pineapple Juice':3.0
                                      }
                               }))
        resp = json.loads(list(ret.response)[0])
        vs = list(resp)
        vs.sort()
        while len([r for r in resp if resp[r]]) > 0:
            time.sleep(0.1)
            ret = self.c.get('/status')
            resp = json.loads(list(ret.response)[0])
        assert len([r for r in resp if resp[r]]) == 0

    def test_stop(self):
        ret = self.c.post('/stop')
        resp = json.loads(list(ret.response)[0])
        vs = list(resp)
        vs.sort()
        assert len([r for r in resp if resp[r]]) == 0

    def test_drinks(self):
        ret = self.c.get('/drinks')
        resp = json.loads(list(ret.response)[0])        
        vs = list(resp)
        assert len(resp) > 0
