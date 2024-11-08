import logging
from time import sleep

import config
from motors import pwm
from sensors import get_yaw
from utils import get_turn_direction, closest_angle

TURN_ERROR = 7

ADDED_DELTA = 10

def microturn():

    while True:
        current_yaw = get_yaw()
        closest = closest_angle(current_yaw)
        delta = get_turn_direction(current_yaw, closest)

        logging.info(f"Need {closest} have {current_yaw} delta {delta}")

        if abs(delta) < TURN_ERROR:
            break


        if (delta)>0:
            delta += ADDED_DELTA
        else:
            delta -= ADDED_DELTA

        turn_one_degree(delta)
        # turn(delta)



def turn(angle):
    logging.info(config.projected_yaw)
    config.projected_yaw += (angle + 360) % 360
    config.projected_yaw = config.projected_yaw % 360

    while True:
        cur_yaw = get_yaw()

        delta = get_turn_direction(cur_yaw, config.projected_yaw)

        logging.info(f"Need {config.projected_yaw} have {cur_yaw} delta {delta}")

        if 70<= abs(delta) <= 105:
            turn_by_constant(delta)
            continue

        if abs(delta) <= TURN_ERROR:
            break

        turn_one_degree(delta)

def turn_one_degree(angle):
    force = 60
    time = 40

    if angle < 0:
        force = -force

    pwm(-force, time, force, time)
    sleep(time/1000 + 0.050)

def turn_by_constant(angle):
    force = 100
    time = abs(angle*2)

    if angle < 0:
        force = -force

    pwm(-force, time, force, time)
    sleep(time/1000 + 0.150)
