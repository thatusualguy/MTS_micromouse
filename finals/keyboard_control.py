import json
import logging

import requests

from backup_2 import shared
from backup_2.shared import real_robotId, real_baseUrl


def forward(dist):
    data = {"id":real_robotId, "direction": "forward", "speed": shared.MOVE_SPEED,
            "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def backwards(dist):
    data = {"id":real_robotId, "direction": "backward","speed": shared.MOVE_SPEED,
            "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def right(turn):
    data = {"id":real_robotId, "speed": shared.ROTATE_SPEED, "direction": "right", "len": abs(int(turn))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def left(turn):
    data = {"id":real_robotId, "speed": shared.ROTATE_SPEED, "direction": "left", "len": abs(int(turn))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


if __name__ == "__main__":

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)


    while True:
        # sense = sensors(no_wait=True)
        # print(sense)
        print("Ожидаю команды... Q - поворот, W - движение. (q 90, w 100)")


        foo =  input().split()
        cmd = str.lower(foo[0])
        if cmd == "q":
            param = int(foo[1])
            if param >0:
                right(param)
            else:
                left(param)
        if cmd == "w":
            param = int(foo[1])
            if param > 0:
                forward(param)
            else:
                backwards(param)
        # if cmd == "s":
            # print(sensors(no_wait=True))