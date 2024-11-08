import json
import logging

from backup_2.girl import girl_pasta
from move import forward
from sensors import setup_sensors, calibrate_north, get_behind_correction
from turn import turn, microturn


def run_from_memory(actions:list[str]):

    correction = 0
    for i, action in enumerate(actions):
        logging.info(f"{i}: {action}")

        action = action.split()

        # microturn()

        if action[0] == "f":
            val = int(action[1])
            val += correction
            forward(val)
            correction = 0

        elif action[0] == "t":
            val = int(action[1])
            turn(val)
            correction = 0
        elif action[0] == "w":
            input("Нажмите для продолжения")
        elif action[0] == "c":
            correction = get_behind_correction()

if __name__ == '__main__':
    FORMAT = "%(funcName)15s - %(message)s"
    logging.basicConfig(format=FORMAT)
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

