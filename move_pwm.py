import logging
from time import sleep

import requests

from hand_rule_solve import sensors
from shared import real_robotId, real_baseUrl

def move(l_pwm, l_time, r_pwm, r_time):
    data = {"id":real_robotId, "l": int(l_pwm), "r":int(r_pwm), "l_time":int(l_time), "r_time":int(r_time)}
    url = real_baseUrl + '/' + "motor"
    print(data)
    requests.put(url, json = data)



def forward(distance):
    start_yaw = sensors()['yaw']

    print("forward ", distance)
    data = sensors()['dist']

    start_distances: int = data[0]
    target_distances: int = data[0] - distance

    max_error = 20
    max_final_speed = 2
    power = 150
    SLEEP = 0.1

    cur_distances = start_distances
    prev_distances = cur_distances
    while True:
        diff = cur_distances - target_distances

        print("Distance diff", diff)


        speed = abs(cur_distances - prev_distances) / SLEEP
        print("speed", speed)

        if abs(diff) < max_error and speed < max_final_speed:
            break

        if speed == 0:
            speed = 0.0000001

        if diff > 0:
            multiplier = 1
        else:
            multiplier = -1

        # magic number yay
        multiplier *= max(0.5, min(1.0, 100 / abs(speed)**2)) # speed
        multiplier *= max(0.5, min(1.0, abs(diff)/120)) # distance
        multiplier *= 2
        if abs(speed) > abs(diff):
            multiplier *= -1
        logging.info("Power", int(power * multiplier))

        move(power * multiplier, SLEEP*1000, power * multiplier, SLEEP*1000)
        sleep(SLEEP)

        prev_distances = cur_distances
        data = sensors()['dist']
        cur_distances: int = data[0]

if __name__ == '__main__':
    forward(130)
