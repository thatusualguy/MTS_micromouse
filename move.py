import logging
from math import floor
from time import sleep

import config
from config import FWD_WAIT_TIME
from motors import pwm
from sensors import get_encoders, get_sensors, get_sensors_raw


def forward(dist_cells):

    for i in range(floor(dist_cells)):
        pwm(100, 300, 100, 300)
        sleep(0.300)
        pwm(-255, 20, -255, 20)

    foo = dist_cells - floor(dist_cells)
    if foo != 0:
        force = 120 * foo
        pwm(force, 300, force, 300)
        sleep(0.200)
        # pwm(-255, 20, -255, 20)




#
    # if dist_cells > config.FWD_MAX_DIST:
    #     dist1 = dist_cells // config.FWD_MAX_DIST
    #     dist1_times = dist_cells // dist1
    #     dist2 = dist_cells % dist1
    #
    #     for i in range(dist1_times):
    #         forward(dist1)
    #     forward(dist2)


    pass

