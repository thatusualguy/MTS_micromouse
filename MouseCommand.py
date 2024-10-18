import time

import requests

from main import baseUrl, token

last_request_timestamp = -10000
cooldown_time = 0.200

class MouseCommands(object):
    _base = "robot-cells"
    _forward = "forward"
    _backwards = "backward"
    _right = "right"
    _left = "left"

    @staticmethod
    def move(direction):
        global last_request_timestamp
        url = baseUrl + MouseCommands._base + '/' + direction + '?token=' + token

        MouseCommands.wait()
        requests.post(url).json()

    @staticmethod
    def wait():
        global last_request_timestamp
        if (last_request_timestamp + cooldown_time) > MouseCommands.get_time():
            sleep_time = last_request_timestamp + cooldown_time - MouseCommands.get_time()
            time.sleep(sleep_time)
        last_request_timestamp = MouseCommands.get_time()

    @staticmethod
    def forward():
        MouseCommands.move(MouseCommands._forward)

    @staticmethod
    def turn_right():
        MouseCommands.move(MouseCommands._right)

    @staticmethod
    def turn_left():
        MouseCommands.move(MouseCommands._left)

    @staticmethod
    def sensors():
        url = baseUrl + MouseCommands._base + '/' + "sensor-data" + '?token=' + token
        MouseCommands.wait()
        return requests.get(url).json()

    @staticmethod
    def get_time():
        return time.time()
