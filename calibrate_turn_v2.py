import json
import logging

import requests

from hand_rule_solve import sensors
from shared import real_robotId, real_baseUrl

if __name__ == "__main__":
    while True:
        turn = int(input())
        start_yaw = sensors()['yaw']

        data = {"id":real_robotId, "direction": "right", "len": abs(int(turn))}
        url = real_baseUrl + '/' + "move"
        logging.info(json.dumps(data))

        end_yaw = sensors()['yaw']
        target = (end_yaw+turn) % 360
        error = target - end_yaw

        logging.info(f"turn {turn}, target {target}, error {error}, start {start_yaw}, end {end_yaw}")