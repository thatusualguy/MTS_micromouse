import time

import requests

from shared import baseUrl, robot_id, gyro_correction

last_request_timestamp = -10000
cooldown_time = 0.200

class MouseCommands(object):


    @staticmethod
    def move(distance):
        pass


    @staticmethod
    def forward(distance):
        data = {"id":robot_id, "direction": "forward", "len": int(distance)}
        url = baseUrl + '/' + "move"
        print(requests.post(url, json = data).text)

    @staticmethod
    def backward(distance):
        data = {"id":robot_id, "direction": "backward", "len": int(distance)}
        url = baseUrl + '/' + "move"
        print(requests.post(url, json = data).text)

    @staticmethod
    def turn_right_90():
        angle = 90
        target =( MouseCommands.get_yaw_now() + 90) % 360
        data = {"id":robot_id, "direction": "right", "len": int(angle+2)}
        url = baseUrl + '/' + "move"
        requests.post(url, json = data)
        print( MouseCommands.get_yaw_now())

    @staticmethod
    def turn_left_90():
        angle = 90
        target =( MouseCommands.get_yaw_now() - 90) % 360
        data = {"id":robot_id, "direction": "right", "len": int(-angle-2)}
        url = baseUrl + '/' + "move"
        requests.post(url, json = data)
        print( MouseCommands.get_yaw_now())

    @staticmethod
    def sensors():
        data = {"id":robot_id,  "type": "all"}
        url = baseUrl + '/' + "sensor"
        res = requests.post(url, json = data).json()
        print(res)
        return res

    @staticmethod
    def get_yaw_raw(sensors_data) -> int:
        return int(sensors_data["imu"]["yaw"])

    @staticmethod
    def get_yaw(sensors_data) -> int:
        return int(sensors_data["imu"]["yaw"]) - gyro_correction

    @staticmethod
    def get_yaw_now():
        return MouseCommands.get_yaw(MouseCommands.sensors())

    @staticmethod
    def get_time():
        return time.time()

    @staticmethod
    def calibrate_gyro():
        global gyro_correction
        cur = MouseCommands.get_yaw_raw(MouseCommands.sensors())
        gyro_correction = cur

