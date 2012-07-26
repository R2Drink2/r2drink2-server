import argh
from app import APP
from r2drink2.valves import Valves
from time import sleep
from utils import *

@argh.command
def run():
    with Valves() as valves:
        APP.valves = valves
        APP.run(APP.config['HOST'], APP.config['PORT'], debug=True)

@argh.command
def clean():
    with Valves() as valves:
        vs = list(get_valve_info())
        vs.sort()
	while True:
            for v in vs:
		valves.start(v)
		sleep(10)
		valves.stop_all()
                sleep(2)



def main():
    parser = argh.ArghParser()
    parser.add_commands([
        run,
        clean
        ])
    parser.dispatch()


if __name__ == '__main__':
    main()
