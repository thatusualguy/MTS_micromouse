from local_move_api import sensors, move
from time import sleep
import json
import shared

SLEEP_const = 0.1


def get_current_yaw():
    return sensors()['rotation_yaw']


def get_delta(a, b):
    # delta of angle a and angle b
    first_delta = max(a, b) - min(a, b)
    second_delta = 360 - first_delta
    return min(first_delta, second_delta)


def calibrate_rotation(need_delta, power=120):  
    print(sensors())
    start_angle = get_current_yaw()
    l, r = 100, 6000
    m = (l+r) // 2
    move(power, m, -power, m)
    sleep(m / 1000)
    new_angle = get_current_yaw()
    current_delta = get_delta(start_angle, new_angle)
    while (l + 1 < r):
        print(current_delta)
        if current_delta > need_delta:
            r = m
        else:
            l = m
        m = (l+r) // 2
        start_angle = new_angle
        move(power, m / 1000, -power, m / 1000)
        sleep(m / 1000 + SLEEP_const)
        new_angle = get_current_yaw()
        current_delta = get_delta(start_angle, new_angle)
        print(l, m, r)
    return r


def test_rotation(time, need_delta, power):
    start_angle = get_current_yaw()
    move(power, time / 1000, -power, time / 1000)
    sleep(time / 1000 + SLEEP_const)
    new_angle = get_current_yaw()

    error = abs(get_delta(start_angle, new_angle) - need_delta)

    print("test time=", time, "power=", power, "getted=", get_delta(start_angle, new_angle), "need=", need_delta)

    return error


def find_params(need_delta):
    EPS = 0.3
    COUNT_TESTS = 10
    STEP = 10

    power = 220

    error = 10 ** 10
    error_accumulator = 0
    while error > EPS:
        power -= STEP
        time = calibrate_rotation(need_delta, power)
        error_accumulator = 0
        for _ in range(COUNT_TESTS):
            error_accumulator += test_rotation(time, need_delta, power)
        error = error_accumulator / COUNT_TESTS
        print(f"power={power} delta={error}")

    print(f'Best params for need_delta={need_delta} is power={power} time={time}')
    return {need_delta: (power, time)}


def calibrate_all_angles(angles: list[int]) -> dict:
    calibrated_data = dict()
    for angle in angles:
        calibrated_data += find_params(angle)
    return calibrated_data

def dump_data(data: dict) -> None:
    with open(shared.local_calibration_filename, 'w') as data_file:
        json.dump(data, data_file)

def load_calibrated_data() -> dict:
    with open(shared.local_calibration_filename, 'r') as data_file:
        data = json.load(data_file)
    return data


if __name__ == "__main__":
    # data = calibrate_all_angles([1, 45, 90, 180])
    data = calibrate_all_angles([90, 70])
    print(data)
    dump_data(data)
    print(load_calibrated_data())
