import logging

import requests

import config
from config import robot_ip, robot_id


def get_sensors_raw(type:str):
    url = f"{robot_ip}/sensors"
    data = {"id": robot_id, "type": type }
    res = requests.post(url, json=data).json()

    logging.info(f"Сенсоры ({type}) \t {res}")
    return res


def get_yaw_raw():
    data = get_sensors_raw("imu")
    return data["imu"]["yaw"]


def get_yaw():
    data = get_sensors_raw("imu")
    return (data["imu"]["yaw"] + 360 - config.yaw_north) % 360

def get_motors():
    data = get_sensors_raw("motor")
    # res = {"left": }
    pass


def get_encoders():
    data = get_sensors_raw("encoders")
    res = {"left": data["encoders"]["left_encoder_delta_sum"],
           "right": data["encoders"]["right_encoder_delta_sum"],}
    return res

def get_sensors():
    pass

def pwm(left, left_t, right, right_t):
    pass
