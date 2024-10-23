from local_move_api import sensors, move
from time import sleep
import json
import shared


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
    left_bound = shared.CALIBRATION_LEFT_BOUND
    right_bound = shared.CALIBRATION_RIGHT_BOUND
    middle = (left_bound+right_bound) // 2
    # / 1000 - because middle is miliseconds
    rotate(power, time=middle / 1000)
    new_angle = get_current_yaw()
    current_delta = get_delta(start_angle, new_angle)
    while (left_bound + 1 < right_bound):
        print(current_delta)
        if current_delta > need_delta:
            right_bound = middle
        else:
            left_bound = middle
        middle = (left_bound+right_bound) // 2
        start_angle = new_angle
        # / 1000 - because middle is miliseconds
        rotate(power, time=middle / 1000)
        new_angle = get_current_yaw()
        current_delta = get_delta(start_angle, new_angle)
        print(left_bound, middle, right_bound)
    # because right_bound is miliseconds
    return right_bound / 1000


def rotate(power, time):
    # time in secs for local
    move(power, time, -power, time)
    sleep(time + shared.MOVE_SLEEP_TIME)



def test_rotation(time, need_delta, power):
    start_angle = get_current_yaw()
    rotate(power=power, time=time)
    new_angle = get_current_yaw()

    error = abs(get_delta(start_angle, new_angle) - need_delta)

    print("test time=", time, "power=", power, "getted=", get_delta(start_angle, new_angle), "need=", need_delta)

    return error


def find_params(need_delta):
    EPS = shared.CALIBRATION_EPS
    COUNT_TESTS = shared.CALIBRATION_COUNT_TESTS
    STEP = shared.CALIBRATION_STEP

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
    return {need_delta: {"power": power, "time": time}}


def calibrate_all_angles(angles: list[int]) -> dict:
    calibrated_data = dict()
    for angle in angles:
        calibrated_data |= find_params(angle)
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
    # data = calibrate_all_angles([90, 70])
    #print(data)
    # dump_data(data)
    print(load_calibrated_data())
