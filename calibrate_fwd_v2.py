import json
import logging

import requests

from hand_rule_solve import sensors
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

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    while True:
        dist = int(input())
        start = sensors()['dist'][0]

        if dist>0:
            forward(dist)
        else:
            backwards(abs(dist))

        end = sensors()['dist'][0]
        real = abs(start - end)
        target = 180

        logging.info(f"dist {dist}, target {target}, real {real}, start {start}, end {end}")