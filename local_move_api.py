import time

import requests

from shared import local_token as token
from shared import local_baseUrl as baseUrl



def move(left_pw, left_time, right_pw, right_time):
    url = baseUrl + 'robot-motors/move'
    params = {
        "token": token,
        "l": int(left_pw),
        "l_time": left_time,
        "r": int(right_pw),
        "r_time": right_time,
    }
    # print(params)
    # print(url)
    ref = requests.post(url, params=params).text
    # print(ref)

def sensors():
    params = {
        "token": token,
    }
    res = requests.get(baseUrl+ "robot-motors/sensor-data", params=params).json()
    hdg = res["rotation_yaw"]
    if hdg<0:
        hdg = 360 + hdg
    res["rotation_yaw"] = hdg

    # 
    # 
    # 
    # print(res)
    return res


def turn_90():

    start_angle = sensors()['rotation_yaw']
    current_angle = sensors()['rotation_yaw']
    end_angle = start_angle + 90
    while abs(current_angle - end_angle)>2:
        diff = current_angle - end_angle
        print(diff)
        # magnitude = 255 * abs(diff)/90 * 2
        magnitude = 255
        if abs(diff) < 10:
            magnitude = abs(diff)*2

        if diff > 0:
            # left
            print("left ", magnitude)
            move(-magnitude, 0.5, magnitude, 0.5)
            pass
        elif diff < 0:
            #right
            print("right ", magnitude)
            move(magnitude, 0.5, -magnitude, 0.5)
            pass
        time.sleep(0.05)
        current_angle = sensors()['rotation_yaw']

    move(120, 1, 255, 1)


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