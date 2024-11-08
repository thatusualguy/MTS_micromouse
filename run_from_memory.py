import json
import logging

from backup_2.girl import girl_pasta
from move import forward
from sensors import setup_sensors, calibrate_north
from turn import turn


def run_from_memory(actions:list[str]):

    for i, action in enumerate(actions):
        logging.debug(f"{i}: {action}")

        action = action.split()

        if action[0] == "f":
            val = int(action[1])
            forward(val)
        elif action[0] == "t":
            val = int(action[1])
            turn(val)

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    setup_sensors()

    print(girl_pasta)
    filename = input("Введите файл лабиринта: ")

    calibrate_north()

    with open(filename, 'r') as fin:
        inp_string = fin.read()
    path = json.loads(inp_string)

    logging.info(path)

    run_from_memory(path)

