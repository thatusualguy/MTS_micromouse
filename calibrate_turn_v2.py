import json
import logging

import requests

from hand_rule_solve import sensors
from shared import real_robotId, real_baseUrl


def right(turn):
    data = {"id":real_robotId, "direction": "right", "len": abs(int(turn))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)

def left(turn):
    data = {"id":real_robotId, "direction": "left", "len": abs(int(turn))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


if __name__ == "__main__":
    while True:
        turn = int(input())
        start_yaw = sensors()['yaw']

        if turn > 0:
            right(turn)
        else:
            left(abs(turn))

        end_yaw = sensors()['yaw']
        target = (start_yaw+90) % 360
        real = abs(start_yaw - end_yaw + 360 ) % 360

        logging.info(f"turn {turn}, target {target}, real {real}, start {start_yaw}, end {end_yaw}")