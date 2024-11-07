import json
import logging
from time import sleep

import requests

from hand_rule_solve import sensors, right
from shared import real_robotId, real_baseUrl

def forward(dist):
    data = {"id":real_robotId, "direction": "forward", "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    requests.put(url, json = data)

def backwards(dist):
    data = {"id":real_robotId, "direction": "backward", "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    requests.put(url, json = data)

CELL_SIZE = 180

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    correction_add = 0
    correction_mult = 1.0

    correction_add = int(input("Correction add: "))
    correction_mult = float(input("Correction mult: "))

    while True:
        start = sensors()['dist'][0]

        should_be_forward = 180//3

        move_dst = abs(start - should_be_forward)

        move_dst += correction_add
        move_dst *= correction_mult

        forward(move_dst)
        sleep(1.0)
        end = sensors()['dist'][0]
        logging.info(f"error {end - should_be_forward}, start_fwd {start}, should_be_fwd {should_be_forward}, end_fwd {end}, move_dst {move_dst}")
        logging.info(f"move_dst_raw {abs(start - should_be_forward)}, correction_add {correction_add}, correction_mult {correction_mult}")
        right()
        right()