import motors
import sensors
from time import sleep
import logging


class RotateCalibration:
    def __init__(self, init_power, left, right, angels=[90]):
        sensors.setup_sensors()
        self.power = init_power
        self.start_left = left
        self.start_right = right
        self.ERROR_AGREEMENT = 5 
        self.COUNT_OF_TESTS_PER_VALUE = 5
        for angle in angels:
            self.need_angle = angle
            self.calibration()

    def calibration(self):
        # need_angle for example 90, 180, 95
        left = self.start_left # time in ms
        right = self.start_right  # time in ms

        while left + 1 < right:
            middle = (left + right) // 2
            error, abs_error = self.test_rotation(middle)
            if (abs_error / self.COUNT_OF_TESTS_PER_VALUE) <= self.ERROR_AGREEMENT:
                print(f'CALIBRATION angle={self.need_angle} power={self.power} middle={middle}')
                return True
            print(left, middle, right)
            if error < 0:
                left = middle
            else:
                right = middle
        return False

    def test_rotation(self, time):
        error = 0
        abs_error = 0
        last_yaw = sensors.get_yaw()

        for _ in range(self.COUNT_OF_TESTS_PER_VALUE):
            motors.pwm(self.power, time, -self.power, time)
            sleep(time / 1000 + 0.3)
            current_yaw = sensors.get_yaw()
            current_angle = self.get_delta(current_yaw, last_yaw)
            current_error = current_angle - self.need_angle
            error += current_error
            abs_error += abs(current_error)
            last_yaw = current_yaw

        return (error, abs_error)

    def get_delta(self, angle_1, angle_2):
        delta_1 = max(angle_1, angle_2) - min(angle_1, angle_2)
        delta_2 = 360 - delta_1
        return min(delta_1, delta_2)


if __name__ == "__main__":
    calib = RotateCalibration(100, 100, 600, angels=[45, 60])


