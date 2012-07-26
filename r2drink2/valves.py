import os
import json
import serial
from utils import *


SERIAL_PORT = "/dev/ttyACM0"

class Valves:
    def __enter__(self):
        print "Starting Valves"
        valve_info = get_valve_info()
        self.status = {}
        for v in valve_info:
            self.status[v] = False
        self._write_serial("C,0,0,0,1\n")
        self.stop_all()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_all()
        print "Ending Valves"
		
    def start(self, v):
        self.status[v] = True
        self._sync_status()

    def stop(self, v):
        self.status[v] = False
        self._sync_status()

    def start_all(self):
        for v in list(self.status):
            self.status[v] = True
        self._sync_status()
        
    def stop_all(self):
        for v in list(self.status):
            self.status[v] = False
        self._sync_status()

    def _write_serial(self, val):
        ser = serial.Serial(port=SERIAL_PORT, baudrate=9600)
        print val
        ser.write(val)
        ser.flush()
        print ser.readline()
        ser.close()

    def _sync_status(self):
        valve_info = get_valve_info()
        port = [0,0,0]
        for v in self.status:
            if self.status[v]:
                for i in range(len(port)):
                    port[i] = port[i]+valve_info[v]['port'][i]
        port = [str(i) for i in port]
        cmd = "O," + (','.join(port)) + "\n"
        self._write_serial(cmd)
