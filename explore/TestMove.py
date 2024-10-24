import time

import requests
from requests import request

from shared import token, real_baseUrl


def move(left_pw, left_time, right_pw, right_time):
    url = real_baseUrl + 'robot-motors/move'
    params = {
        "token": token,
        "l": int(left_pw),
        "l_time": left_time,
        "r": int(right_pw),
        "r_time": right_time,
    }
    print(params)
    requests.post(url, params=params)

def sensors():
    params = {
        "token": token,
    }
    res = requests.get(real_baseUrl + "robot-motors/sensor-data", params=params).json()
    hdg = res["rotation_yaw"]
    if hdg<0:
        hdg = 360 + hdg
    res["rotation_yaw"] = hdg

    # print(res)
    return res




# def key_control():
#     while(True):


# move(243, 1.1, -243, 1.1)
# move(-243, 1.1, -243, 1.1)
# move(-120, 0.3, -120, 0.3)
# move(120, 0.5, 120, 0.5)
# move(0, 6, -255/2, 6)

# time.sleep(1)

# wait = 1
# move(120/2, wait,120/2,wait)
# time.sleep(wait)
# move(120/2, wait,-10,wait)
# time.sleep(wait)
# move(120, wait,-10,wait)
# time.sleep(wait)
# move(120, wait,120,wait)

# sensors()