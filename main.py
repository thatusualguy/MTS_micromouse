import logging
from time import sleep

from motors import pwm
from sensors import setup_sensors, get_sensors

def fwd():
    # 1 клетка почти
    pwm(100, 300, 100, 300)
    sleep(0.330)
    pwm(-255, 20, -255, 20)

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    setup_sensors()
    print(get_sensors())

    # pwm(-140, 137, 140, 137)
    # pwm(-110, 161, 110, 161)
    # pwm(110, 161, -110, 161)

    fwd()

