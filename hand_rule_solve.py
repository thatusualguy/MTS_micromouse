import json
import logging
import time
from math import radians, cos, sin
from typing import Any


import requests

import shared
from girl import girl_pasta
from shared import real_robotId, TYPE, real_baseUrl, local_baseUrl, local_token, wait_time

sev_yaw = 0

def sensors_raw() -> dict[Any]:
    if TYPE == "real":
        data = {"id":real_robotId, "type": "all"}
        url = real_baseUrl + '/' + "sensor"
        res = requests.post(url, json = data).json()
        return res
    elif TYPE == "local":
        url = local_baseUrl + 'robot-motors/sensor-data'
        params = { "token": local_token}
        res = requests.get(url, params = params).json()
        return res

def sensors() -> dict[str, dict[int, int] | int]:
    time_to_sleep =  shared.prev_request+wait_time - time.time()
    if time_to_sleep > 0:
        print("sleeping", time_to_sleep)
        time.sleep(time_to_sleep)
    shared.prev_request = time.time()

    if TYPE == "real":
        data = sensors_raw()

        values = [
            data['laser']["1"],
            data['laser']["2"],
            data['laser']["4"],
            data['laser']["5"],
            data['laser']["3"],
            data['laser']["6"],
        ]
        directions = [
            180, 270, 0, 90, 45, 360-45
        ]

        result: dict[str, dict[int, int] | int] = dict()
        result['dist'] = dict(zip(directions, values))
        result['yaw_raw'] = data["imu"]['yaw']
        result['yaw']  = (result['yaw_raw'] + 360 - sev_yaw) % 360
        logging.info(result)
        return result
    elif TYPE == "local":
        data = sensors_raw()

        values = [
            data['front_distance'],
            data['right_side_distance'],
            data['left_side_distance'],
            data['back_distance'],
        ]
        directions = [
            0, 90, 270, 180
        ]

        result: dict[str, dict[int, int] | int] = dict()
        result['dist'] = dict(zip(directions, values))
        result['yaw_raw'] = int(data["rotation_yaw"])
        result['yaw']  = (result['yaw_raw'] + 360 - sev_yaw) % 360
        return result

def forward():
    dist = 130
    data = {"id":real_robotId, "direction": "forward", "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def right():
    turn = 90
    data = {"id":real_robotId, "direction": "right", "len": abs(int(turn))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)

def left():
    turn = 90
    data = {"id":real_robotId, "direction": "left", "len": abs(int(turn))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def backwards():
    dist = 130
    data = {"id":real_robotId, "direction": "backward", "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)



class AA:

    isRightHand = False

    def __init__(self, isRightHand):
        self.WE_ARE_IN_CENTER = False
        global sev_yaw

        self.current_y = 15
        self.current_x = 0
        sev_yaw = sensors()['yaw_raw']

        self.isRightHand = isRightHand
        self.autopilot()

    def autopilot(self):
        logging.info(f"Autopilot in {self.current_x} {self.current_y} start")
        for rotation in self.get_neighbours():
            if rotation == 'left':
                self.rotate_left()
            elif rotation == 'right':
                self.rotate_right()
            self.move_forward()
            self.autopilot()
            if self.WE_ARE_IN_CENTER or self.we_are_in_center():
                return
            self.move_back()
            if rotation == 'right':
                self.rotate_left()
            elif rotation == 'left':
                self.rotate_right()
        logging.info(f"Autopilot in {self.current_x} {self.current_y} end")
    
    def rotate_left(self):
        left()
    
    def rotate_right(self):
        right()
    
    def move_forward(self):
        dx, dy = self.get_by_yaw()
        self.current_x += dx
        self.current_y += dy
        forward()
    
    def move_back(self):
        dx, dy = self.get_by_yaw()
        self.current_x -= dx
        self.current_y -= dy
        backwards()

    def get_neighbours(self):
        neighbours = []
        sensor_data = sensors()

        if self.isRightHand:
            if sensor_data['dist'][90] > 150:
                neighbours.append('right')
        else:
            if sensor_data['dist'][270] > 150:
                neighbours.append('left')

        if sensor_data['dist'][0] > 150:
            neighbours.append('forward')

        if self.isRightHand:
            if sensor_data['dist'][270] > 150:
                neighbours.append('left')
        else:
            if sensor_data['dist'][90] > 150:
                neighbours.append('right')

        return neighbours

    def we_are_in_center(self):
        res = self.current_x in (7, 8) and self.current_y in (7, 8)
        # sensor_data = sensors()
        # res =  sensor_data['dist'][0] > 150 and sensor_data['dist'][90] > 150 and sensor_data['dist'][45] > 150
        if res:
            logging.info(f"We are in center!!!")
            self.WE_ARE_IN_CENTER = True
        return res


    def get_by_yaw(self):
        sensor_data = sensors()
        dx = - round(1 * cos(radians(sensor_data['yaw'])))
        dy = round(1 * sin(radians(sensor_data['yaw'])))

        logging.info(f"yaw: {sensor_data['yaw']}, dx: {dx}, dy: {dy}")
        return dx, dy


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    print(girl_pasta)
    start_RightHand = True
    start_RightHand = 1 == int(input("С какой руки начать? 1 - правая"))
    input("Вы готовы, дети?")
    AA(start_RightHand)
    input("Вы готовы, дети?")
    AA(not start_RightHand)
    print(girl_pasta)
