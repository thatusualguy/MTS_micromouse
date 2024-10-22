import time

import requests

from shared import baseUrl, robot_id, gyro_correction

last_request_timestamp = -10000
cooldown_time = 0.200

class MouseCommands(object):


    @staticmethod
    def move(left, left_time, right, right_time):
        data = {"id":robot_id, "l": int(left), "r":int(right), "l_rime":left_time, "r_rime":right_time}
        url = baseUrl + '/' + "motor"
        print(requests.put(url, json = data).text)


    @staticmethod
    def forward(distance):
        print("forward ", distance)
        data = {"id":robot_id, "direction": "forward", "len": int(distance)}
        url = baseUrl + '/' + "move"
        print(requests.put(url, json = data).text)

    @staticmethod
    def backward(distance):
        print("distance ", distance)
        data = {"id":robot_id, "direction": "backward", "len": int(distance)}
        url = baseUrl + '/' + "move"
        print(requests.put(url, json = data).text)

    @staticmethod
    def turn_right_90():
        start_angle = MouseCommands.get_yaw_now()
        current_angle = MouseCommands.get_yaw_now()
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
                MouseCommands.move(-magnitude, 200, magnitude, 200)
                pass
            elif diff < 0:
                #right
                print("right ", magnitude)
                MouseCommands.move(magnitude, 200, -magnitude, 200)
                pass
            time.sleep(0.2)
            current_angle = MouseCommands.get_yaw_now()

    @staticmethod
    def turn_left_90():
        # print("left")
        # angle = 90
        # target =( MouseCommands.get_yaw_now() - 90) % 360
        # data = {"id":robot_id, "direction": "left", "len": int(angle+2)}
        # url = baseUrl + '/' + "move"
        # requests.put(url, json = data)
        # print( MouseCommands.get_yaw_now())

        start_angle = MouseCommands.get_yaw_now()
        current_angle = MouseCommands.get_yaw_now()
        end_angle = start_angle + 270
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
                MouseCommands.move(-magnitude, 200, magnitude, 200)
                pass
            elif diff < 0:
                #right
                print("right ", magnitude)
                MouseCommands.move(magnitude, 200, -magnitude, 200)
                pass
            time.sleep(0.2)
            current_angle = MouseCommands.get_yaw_now()

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

