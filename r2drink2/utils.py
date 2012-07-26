import os
import json

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
VALVE_INFO_FILE = os.path.join(STATIC_DIR, 'valve_info.json')
DRINK_INFO_FILE = os.path.join(STATIC_DIR, 'drink_info.json')

def get_valve_info():
    with open(VALVE_INFO_FILE, 'r') as f:
        valve_info = json.load(f)
    return valve_info
    

def get_drink_info():
    with open(DRINK_INFO_FILE, 'r') as f:
        drink_info = json.load(f)
    return drink_info
