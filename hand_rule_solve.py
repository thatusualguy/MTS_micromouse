import json
import logging
import time
from math import radians, cos, sin
from time import sleep
from typing import Any


import requests

import shared
from girl import girl_pasta
from shared import real_robotId, TYPE, real_baseUrl, local_baseUrl, local_token, wait_time

sev_yaw = 0


def pwm_move(left, left_time_ms, right, right_time_ms):
    data = {"id":real_robotId, "l": int(left), "r":int(right), "l_time":int(left_time_ms), "r_time":int(right_time_ms)}
    url = real_baseUrl + '/' + "motor"
    logging.info(json.dumps(data))
    requests.put(url, json = data)


def sensors_raw() -> dict[Any]:
    data = {"id":real_robotId, "type": "all"}
    url = real_baseUrl + '/' + "sensor"
    res = requests.post(url, json = data).json()
    return res


def sensors(no_wait = False) -> dict[str, dict[int, int] | int]:
    if not no_wait:
        sleep(wait_time)

    data = sensors_raw()

    values = [
        data['laser']["1"],
        data['laser']["2"],
        data['laser']["3"],
        data['laser']["4"],
        data['laser']["5"],
        data['laser']["6"],
    ]

    directions = [
        180, 90, 45, 0, 360-45, 270
    ]

    result: dict[str, dict[int, int] | int] = dict()
    result['dist'] = dict(zip(directions, values))
    result['yaw_raw'] = data["imu"]['yaw']
    result['yaw']  = (result['yaw_raw'] + 360 - sev_yaw) % 360
    result['motor'] =  data["motor"]
    logging.info(result)
    return result

def forward():
    dist = shared.FORWARD_DIST
    data = {"id":real_robotId, "direction": "forward", "speed": shared.MOVE_SPEED,
            "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def backwards():
    dist = shared.BACK_DIST
    data = {"id":real_robotId, "direction": "backward","speed": shared.MOVE_SPEED,
            "len": abs(int(dist))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def right():
    turn = 90

    yaw = sensors(True)['yaw'] + turn
    closest = closest_angle(yaw)
    delta = get_turn_direction(yaw, closest)

    data = {"id":real_robotId, "speed": shared.ROTATE_SPEED, "direction": "right", "len": abs(int(turn+delta))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)


def left():
    turn = 90

    yaw = sensors(True)['yaw'] - turn
    closest = closest_angle(yaw)
    delta = get_turn_direction(yaw, closest)

    data = {"id":real_robotId, "speed": shared.ROTATE_SPEED, "direction": "left", "len": abs(int(turn-delta))}
    url = real_baseUrl + '/' + "move"
    logging.info(json.dumps(data))
    print(requests.put(url, json = data).text)

def get_turn_direction(start, target):
    turn = (target - start) % 360
    if turn > 180:
        turn -= 360
    return int(turn)


def closest_angle(angle):
    return  (angle+45)//90* 90 % 360


class AA:

    isRightHand = False

    def __init__(self, isRightHand=True):
        self.WE_ARE_IN_CENTER = False
        global sev_yaw

        self.current_y = 15
        self.current_x = 0
        sev_yaw = sensors()['yaw_raw']

        self.move_history = []

        self.isRightHand = isRightHand
        # self.autopilot()

    def autopilot(self):
        self.move_history = []
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

    def run_by_history(self, skip_moves = 0):

        for move in self.move_history[skip_moves:]:
            if move == 'left':
                self.rotate_left(write_to_history=False)
            if move == 'right':
                self.rotate_right(write_to_history=False)
            if move == 'forward':
                self.move_forward(write_to_history=False)
            if move == 'back':
                self.move_back(write_to_history=False)

            while True:
                motor = sensors()['motor']
                if motor["right_pwm"] == 0 and motor["left_pwm"] == 0:
                    break
                time.sleep(0.05)

    def rotate_left(self, write_to_history=True):
        if write_to_history:
            self.move_history.append('left')
        left()
    
    def rotate_right(self, write_to_history=True):
        if write_to_history:
            self.move_history.append('right')
        right()
    
    def move_forward(self, write_to_history=True):
        if write_to_history:
            self.move_history.append('forward')
        dx, dy = self.get_by_yaw()
        self.current_x += dx
        self.current_y += dy
        forward()
    
    def move_back(self, write_to_history=True):
        if write_to_history:
            self.move_history.append('back')
        dx, dy = self.get_by_yaw()
        self.current_x -= dx
        self.current_y -= dy
        backwards()

    def get_neighbours(self):
        sleep(0.8)
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
        # res = self.current_x in (7, 8) and self.current_y in (7, 8)
        sensor_data = sensors()
        res =  (sensor_data['dist'][0] > 180 and sensor_data['dist'][90] > 180 and sensor_data['dist'][45] > 180) or  (sensor_data['dist'][0] > 180 and sensor_data['dist'][270] > 180 and sensor_data['dist'][360-45] > 180)
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

    def dump_history(self, filename="move_history.json"):
        with open(filename, 'w') as fout:
            fout.write(json.dumps(self.move_history))
        logging.info('write history in file')

    def load_history(self, filename="move_history.json"):
        with open(filename, 'r') as fin:
            inp_string = fin.read()
            self.move_history = json.loads(inp_string)
        logging.info('readed history from file')

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    print(girl_pasta)

    nostrafe = 1 == int(input("Без стрейфов? 1 - без"))

    start_RightHand = True
    start_RightHand = 1 == int(input("С какой руки начать? 1 - правой"))
    robot = AA(start_RightHand)
    input("Вы готовы, дети?")
    robot.autopilot()
    robot.dump_history()

    is_autopilot = 1 == int(input("autopilot or not? 1 - autopilot"))
    if is_autopilot:
        robot = AA(start_RightHand)
        robot.autopilot()
        robot.dump_history()
    else:
        robot.run_by_history()

    is_autopilot = 1 == int(input("autopilot or not? 1 - autopilot"))
    if is_autopilot:
        robot = AA(start_RightHand)
        robot.autopilot()
        robot.dump_history()
    else:
        robot.run_by_history()
    
    print(girl_pasta)

