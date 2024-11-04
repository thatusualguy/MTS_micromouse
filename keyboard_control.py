import json
import logging

import requests

from hand_rule_solve import sensors, forward
from shared import real_robotId, real_baseUrl


def forward(dist):
    data = {"id":real_robotId, "direction": "forward", "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def backwards(dist):
    data = {"id":real_robotId, "direction": "backward", "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


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

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)


    while True:
        print(sensors(no_wait=True))
        print("Ожидаю команды... Q - поворот, W - движение. (q 90, w 100)")
        foo =  input().split()
        cmd = str.lower(foo[0])
        param = int(foo[1])
        if cmd == "q":
            if param >0:
                right(param)
            else:
                left(param)
        if cmd == "w":
            if param > 0:
                forward(param)
            else:
                backwards(param)
        if cmd == "s":
            print(sensors(no_wait=True))