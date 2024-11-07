import logging

import requests

import config
from config import robot_id, robot_ip


def pwm(left, left_t, right, right_t):
    # ограничение максимального времени
    left_t = min(left_t, config.MAX_RUN_TIME)
    right_t = min(right_t, config.MAX_RUN_TIME)

    # перепутано направление моторов
    left *= -1
    right *= -1

    url = f"{robot_ip}/motor"
    data = {"id":robot_id, "l": int(left), "r":int(right), "l_time":int(left_t), "r_time":int(right_t)}
    logging.info(data)
    print(requests.put(url, json = data).text)