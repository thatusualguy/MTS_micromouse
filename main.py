import logging
from time import sleep

from backup_2.shared import calibrated_turns
from motors import pwm
from sensors import setup_sensors, get_sensors, get_yaw, calibrate_north, get_behind_correction
from turn import turn, microturn, turn_one_degree


def fwd():
    # 1 клетка почти
    pwm(100, 300, 100, 300)
    sleep(0.300)
    pwm(-255, 20, -255, 20)

if __name__ == '__main__':
    FORMAT = "%(funcName)15s - %(message)s"
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)

    setup_sensors()
    calibrate_north()

    # input()

    # print(get_sensors())
    print(get_yaw())


    foo = get_behind_correction()
    if foo != 0:
        force = 150 * foo
        pwm(force, 300, force, 300)
        sleep(0.200)
        # pwm(-255, 20, -255, 20)


# turn(90)

    # microturn()

    # turn_one_degree(1)
    # pwm(-140, 137, 140, 137)
    # pwm(-110, 161, 110, 161)
    # pwm(50, 300, 50, 300)

    # angle = 81

    # pwm(50, 40, -50, 40)

    # sleep(0.5)
    # print(get_yaw())
    # fwd()

