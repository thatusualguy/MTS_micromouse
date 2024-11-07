import json
import logging

import requests

from config import robot_ip, robot_id


def pwm(left, left_t, right, right_t):
    data = {"id":robot_id, "l": int(left), "r":int(right), "l_time":int(left_t), "r_time":int(right_t)}
    url = robot_ip + '/' + "motor"
    logging.info(json.dumps(data))
    requests.put(url, json = data)
    pass