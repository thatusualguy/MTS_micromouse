import json
import time
from time import sleep
from typing import Any

import requests

from backup_2 import shared
from backup_2.hand_rule_solve import pwm_move
from backup_2.shared import real_baseUrl, real_robotId, gyro_correction, TYPE, local_baseUrl, local_token, real_CELL_SIZE, \
    local_CELL_SIZE, real_robotSize, local_robotSize
from finals.sensors import get_yaw


def get_turn_direction(start, target):
    turn = (target - start) % 360
    if turn > 180:
        turn -= 360
    return int(turn)

prev_request = -100
wait_time = 1.400



class MouseCommands(object):

    @staticmethod
    def move(left, left_time_ms, right, right_time_ms):
        if TYPE == "real":
            data = {"id":real_robotId, "l": int(left), "r":int(right), "l_time":int(left_time_ms), "r_time":int(right_time_ms)}
            url = real_baseUrl + '/' + "motor"
            print(data)
            requests.put(url, json = data)
        elif TYPE == "local":
            url = local_baseUrl + 'robot-motors/move'
            params = {
                "token": local_token,
                "l": int(left),
                "l_time": left_time_ms / 1000.0,
                "r": int(right),
                "r_time": right_time_ms / 1000.0,
            }
            requests.post(url, params=params)

    @staticmethod
    def forward_real(dist):
        data = {"id":real_robotId, "direction": "forward", "len": abs(int(dist))}
        url = real_baseUrl + '/' + "move"
        print(requests.put(url, json = data).text)

    @staticmethod
    def back_real(dist):
        data = {"id":real_robotId, "direction": "backwards", "len": abs(int(dist))}
        url = real_baseUrl + '/' + "move"
        print(requests.put(url, json = data).text)

    @staticmethod
    def forward(distance):
        start_yaw = MouseCommands.sensors()['yaw']

        print("forward ", distance)
        data = MouseCommands.sensors()['dist']

        start_distances: dict[int, int] = {0: data[0], 180: data[180]}
        target_distances: dict[int, int] = {0: data[0] - distance, 180: data[180] + distance}

        # for i in range(len(start_distances), 0 , -1):
        #     if start_distances[i] > 5000:
        #         start_distances.pop(i)
        #         target_distances.pop(i)
        #
        #
        # if len(start_distances) == 0:
        #     print("Error on all sensors")
        #     exit(1)

        for i in target_distances.values():
            if i < 10:
                print("Moving too far!")
                exit(1)

        max_error = 20
        max_final_speed = 2
        power = 150
        SLEEP = 0.1

        cur_distances = start_distances
        prev_distances = cur_distances
        while True:
            diff = (cur_distances[0] - target_distances[0]) / 2 + (target_distances[180] - cur_distances[180]) / 2

            # print("Distance diff", diff)

            if TYPE =="local":
                speed = abs((cur_distances[0] - prev_distances[0]) / 2 + (prev_distances[180] - cur_distances[180]) / 2) / SLEEP
                # print("speed", speed)

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

                if abs(speed) > abs(diff):
                    multiplier *= -1

                # print("Power", int(power * multiplier))

                MouseCommands.move(power * multiplier, SLEEP*1000, power * multiplier, SLEEP*1000)
                sleep(SLEEP)

            if TYPE =="real":
                if abs(diff)<max_error:
                    break

                data = {"id":real_robotId, "direction": "forward", "len": abs(int(diff))}
                if diff>0:
                    data["direction"] = "forward"
                else:
                    data["direction"] = "backward"

                url = real_baseUrl + '/' + "move"
                print(data)
                print(requests.put(url, json = data).text)

            prev_distances = cur_distances
            data = MouseCommands.sensors()['dist']
            cur_distances: dict[int, int] = {0: data[0], 180: data[180]}

        MouseCommands.turn_to(start_yaw)

    @staticmethod
    def forward_one():
        distance = 0

        if TYPE == "real":
            distance = real_CELL_SIZE
        elif TYPE == "local":
            distance=local_CELL_SIZE

        forward = MouseCommands.sensors()['dist'][0]
        if forward < 250:
            distance = forward - 50

        MouseCommands.forward(distance)

    @staticmethod
    def backward(distance):
        pass

    @staticmethod
    def turn(degrees: int):
        start_yaw = MouseCommands.sensors()['yaw']
        target_yaw = (start_yaw + degrees ) % 360
        if target_yaw < 0:
            target_yaw += 360

        diff = get_turn_direction(start_yaw, target_yaw)
        while abs(diff) > 3:
            direction = 1
            if diff < 0:
                direction = -1
                diff *= -1

            for degrees, params in shared.calibrated_turns.items():
                print(diff, degrees)
                for i in range(diff // degrees):
                    MouseCommands.rotate(params["power"]*direction, params["time"])
                diff %= degrees
            diff = get_turn_direction(MouseCommands.sensors()['yaw'], target_yaw)

    @staticmethod
    def turn_to(target:int):
        current = MouseCommands.sensors()['yaw']
        turn = get_turn_direction(current, target)
        if turn != 0:
            MouseCommands.turn(turn)

    @staticmethod
    def turn_right_90():
        target = round((MouseCommands.sensors()['yaw'] + 90)/90)* 90
        MouseCommands.turn_to(target)

    @staticmethod
    def turn_left_90():
        target = round((MouseCommands.sensors()['yaw'] + 270)/90)* 90 % 360
        MouseCommands.turn_to(target)


    @staticmethod
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

    @staticmethod
    def sensors() -> dict[str, dict[int, int] | int]:
        global prev_request
        time_to_sleep =  prev_request+wait_time - time.time()
        if time_to_sleep > 0:
            print("sleeping", time_to_sleep)
            time.sleep(time_to_sleep)
        prev_request = time.time()

        if TYPE == "real":
            data = MouseCommands.sensors_raw()

            values = [
                data['laser']["1"],
                data['laser']["2"],
                data['laser']["4"],
                data['laser']["5"],
                # data['laser']["3"],
                # data['laser']["6"],
            ]
            directions = [
                # 180, 270, 0, 90, 45,360-45
                180, 270, 0, 90,
            ]

            result: dict[str, dict[int, int] | int] = dict()
            result['dist'] = dict(zip(directions, values))
            result['yaw_raw'] = data["imu"]['yaw']
            result['yaw'] = result['yaw_raw'] + gyro_correction
            return result
        elif TYPE == "local":
            data = MouseCommands.sensors_raw()

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

            corrected = (result['yaw_raw'] + gyro_correction) % 360
            if corrected < 0:
                corrected = 360 - corrected
            result['yaw'] = corrected

            return result

    @staticmethod
    def center():
        remember_yaw = MouseCommands.sensors()['yaw']
        centering_error = 20


        cell_size = 0
        if TYPE == "real":
            cell_size = real_CELL_SIZE
        elif TYPE == "local":
            cell_size = local_CELL_SIZE

        robot_size = 0
        if TYPE == "real":
            robot_size = real_robotSize
        elif TYPE == "local":
            robot_size = local_robotSize

        data = MouseCommands.sensors()['dist']

        for direction, distance in data.items():
            if distance < cell_size:
                diff = distance - (cell_size - robot_size)/2
                if abs(diff) > centering_error:
                    target_yaw_local = 0
                    if diff < 0:
                        target_yaw_local = direction
                    if diff > 0:
                        target_yaw_local = (direction + 180) % 360
                    target_yaw_global = (target_yaw_local + remember_yaw ) % 360
                    MouseCommands.turn_to(target_yaw_global)
                    MouseCommands.forward(abs(diff))
                    MouseCommands.turn_to(remember_yaw)


    @staticmethod
    def sensors_to_blocks() -> dict[int, int]:
        data = MouseCommands.sensors()
        result = dict()
        print(data)
        for k, v in data["dist"].items():
            if k in [45, 360-45]:
                print("Excluded", k)
                continue

            if v < 130:
                result[k]=0
            else:
                result[k]=1

        return result

    @staticmethod
    def calibrate_gyro():
        cur = MouseCommands.sensors()["yaw"]
        shared.gyro_correction = -cur


    @staticmethod
    def calibrate_basic_rotations():
        # res = MouseCommands.calibrate_all_angles([90, 45, 8, 2, 1])
        res = MouseCommands.calibrate_all_angles([90, 45, 8, 2, 1])
        print("Calibrated turns:", res)
        shared.calibrated_turns = res
        MouseCommands.dump_data(shared.calibrated_turns)
        MouseCommands.turn_to(0)

    @staticmethod
    def get_delta(a, b):
        # delta of angle a and angle b
        first_delta = max(a, b) - min(a, b)
        second_delta = 360 - first_delta
        return min(first_delta, second_delta)

    @staticmethod
    def calibrate_rotation(need_delta, power=120):
        start_angle = get_yaw()
        left_bound = shared.CALIBRATION_LEFT_BOUND
        right_bound = shared.CALIBRATION_RIGHT_BOUND
        middle = (left_bound+right_bound) // 2
        pwm_move(power, middle, -power, middle)
        new_angle = get_yaw()
        current_delta = MouseCommands.get_delta(start_angle, new_angle)
        while left_bound + 1 < right_bound:
            sleep(0.5)
            print(current_delta)
            if current_delta > need_delta:
                right_bound = middle
            else:
                left_bound = middle
            middle = (left_bound+right_bound) // 2
            start_angle = new_angle
            pwm_move(power, middle, -power, middle)
            new_angle = get_yaw()
            current_delta = MouseCommands.get_delta(start_angle, new_angle)
            print(left_bound, middle, right_bound)
        return right_bound

    @staticmethod
    def get_current_yaw():
        return get_yaw()

    @staticmethod
    def rotate(power, time_s):
        MouseCommands.move(power, time_s, -power, time_s)
        sleep(time_s/1000 + shared.MOVE_SLEEP_TIME)


    @staticmethod
    def test_rotation(time, need_delta, power):
        sleep(0.5)
        start_angle = MouseCommands.get_current_yaw()
        MouseCommands.rotate(power=power, time_s=time)
        new_angle = MouseCommands.get_current_yaw()

        error = abs(MouseCommands.get_delta(start_angle, new_angle) - need_delta)

        print("test time=", time, "power=", power, "getted=", MouseCommands.get_delta(start_angle, new_angle), "need=", need_delta)

        return error

    @staticmethod
    def find_params(need_delta):
        EPS = shared.CALIBRATION_EPS
        COUNT_TESTS = shared.CALIBRATION_COUNT_TESTS
        STEP = shared.CALIBRATION_STEP

        power = shared.CALIBRATION_START_POWER

        error = 10 ** 10
        error_accumulator = 0
        while error > EPS:
            power -= STEP
            time = MouseCommands.calibrate_rotation(need_delta, power)
            error_accumulator = 0
            for _ in range(COUNT_TESTS):
                error_accumulator += MouseCommands.test_rotation(time, need_delta, power)
            error = error_accumulator / COUNT_TESTS
            print(f"power={power} delta={error}")

        print(f'Best params for need_delta={need_delta} is power={power} time={time}')
        return {need_delta: {"power": power, "time": time}}


    @staticmethod
    def calibrate_all_angles(angles: list[int]) -> dict:
        calibrated_data = dict()
        for angle in angles:
            calibrated_data |= MouseCommands.find_params(angle)
            MouseCommands.dump_data(calibrated_data)
        return calibrated_data

    @staticmethod
    def dump_data(data: dict) -> None:
        with open(shared.local_calibration_filename, 'w') as data_file:
            json.dump(data, data_file)

    @staticmethod
    def load_calibrated_data() -> None:
        with open(shared.local_calibration_filename, 'r') as data_file:
            data = json.load(data_file)

            res = dict()
            for k, v in data.items():
                res[int(k)] = v

            shared.calibrated_turns = res





















