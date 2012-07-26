import os
from flask import *
import r2drink2
import json
import threading
import time
from utils import *
from datetime import datetime


APP = Flask(__name__)
APP.config.from_pyfile('config.cfg')
APP.config.setdefault('HOST', os.environ.get('HOST', '0.0.0.0'))
APP.config.setdefault('PORT', int(os.environ.get('PORT', 80)))




VALVE_LOCK = threading.Lock()

def pour_valve(valve, duration):
    VALVE_LOCK.acquire()
    try:
        APP.valves.start(valve)
    finally:
        VALVE_LOCK.release()
    time.sleep(duration)
    VALVE_LOCK.acquire()
    try:
        APP.valves.stop(valve)
    finally:
        VALVE_LOCK.release()
    

@APP.route('/')
def default_page():
    return r2drink2.__version__


@APP.route('/version', methods=['GET'])
def version_info():
    return r2drink2.__version__


@APP.route('/pour', methods=['POST'])
def pour():
    valve_info = get_valve_info()
    valve_drink_map = {}
    for v in valve_info:
        valve_drink_map[valve_info[v]['ingredient']] = v
    req = json.loads(request.data)
    req['timestamp'] = str(datetime.now())
    with open("log.txt","a") as l:
        l.write(json.dumps(req))
        l.write("\n")
    volume = float(req['qty'])
    r_total = sum([float(req['ingredients'][i]) for i in req['ingredients']])
    ingredients = {}
    for i in req['ingredients']:
        ratio = float(req['ingredients'][i]) / r_total
        v = valve_drink_map[i]
        if ratio > 0:
            ingredients[v] = volume * ratio * valve_info[v]['rate']
    for v,d in ingredients.iteritems():
        thread = threading.Thread(target=pour_valve,
                                  args=(v, d))
        thread.start()
    time.sleep(0.1)
    return status()

@APP.route('/stop', methods=['POST'])
def stop():
    valve_info = get_valve_info()
    VALVE_LOCK.acquire()
    try:
        APP.valves.stop_all()
    finally:
        VALVE_LOCK.release()
    return status()


@APP.route('/status', methods=['GET'])
def status():
    VALVE_LOCK.acquire()
    try:
        return json.dumps(APP.valves.status)
    finally:
        VALVE_LOCK.release()
    
@APP.route('/drinks', methods=['GET'])
def drinks():
    return json.dumps(get_drink_info())

@APP.route('/ingredients', methods=['GET'])
def ingredients():
    valve_info = get_valve_info()
    ks = list(valve_info)
    ks.sort()
    return json.dumps([valve_info[v]['ingredient'] for v in ks])

