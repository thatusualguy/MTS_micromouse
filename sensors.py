import logging
from time import sleep

import requests

import config
from config import robot_ip, robot_id, SENSOR_REFRESH_RATE


# curl -X POST -H "Content-Type: application/json" -d '{"id": "F535AF9628574A53", "interval": 20, "enabled_sensors": ["left", "right", "forward"]}' http://192.168.69.144/sensor_config
def setup_sensors(refresh_rate_ms = SENSOR_REFRESH_RATE):
    url = f"{robot_ip}/sensor_config"
    data = {"id": robot_id, "interval": refresh_rate_ms, "enabled_sensors": ["left", "right", "forward", "backward"]}
    requests.post(url, json=data)
    logging.info(f"Конфиг сенсоров {data}")


def calibrate_north():
    config.yaw_north = 0
    config.yaw_north = get_yaw()
    logging.info(f"Север {config.yaw_north}")

def get_sensors_raw(type_: str):
    url = f"{robot_ip}/sensor"
    data = {"id": robot_id, "type": type_}
    res = requests.post(url, json=data)
    res = res.json()
    logging.info(f"Сенсоры ({type_}) \t {res}")
    return res


def get_yaw_raw():
    data = get_sensors_raw("imu")
    return data["imu"]["yaw"]


def get_yaw():
    data = get_sensors_raw("imu")
    return (data["imu"]["yaw"] + 360 - config.yaw_north) % 360


def get_motors():
    data = get_sensors_raw("motor")
    Exception("Not implemented")
    pass


def get_encoders():
    data = get_sensors_raw("encoders")
    res = {"left":  config.MOTOR_DIRECTION * int(data["encoders"]["left_encoder_delta_sum"]),
           "right":  config.MOTOR_DIRECTION * int(data["encoders"]["right_encoder_delta_sum"]), }
    return res


def get_sensors():
    sleep(config.SENSOR_SLEEP / 1000)

    data = get_sensors_raw("laser")
    lasers = [
        data["laser"]["forward"],
        data["laser"]["right"],
        data["laser"]["backward"],
        data["laser"]["left"],
    ]
    directions = [
        0, 90, 180, 270
    ]

    res = dict(zip(directions, lasers))

    return res


