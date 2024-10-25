from Point import Point

TYPE = "local"
# TYPE = "real"


center = [Point(7, 7), Point(7, 8), Point(8, 8), Point(8, 7), ]
graph: dict[Point, list[Point]] = dict()

real_baseUrl = "http://192.168.68.134"
real_robotId = "3536AF962E7A4A53"
gyro_correction = 0
calibration_filename = 'calibrated_data.json'
real_CELL_SIZE = 180
real_robotSize = 75

local_calibration_filename = 'local_calibrated_data.json'
local_baseUrl = "http://127.0.0.1:8801/api/v1/"
local_token = 'some-token-code'
local_CELL_SIZE = 180
local_robotSize = 75

MOVE_SLEEP_TIME = 0.1
CALIBRATION_EPS = 0.5
CALIBRATION_COUNT_TESTS = 10
CALIBRATION_STEP = 10
CALIBRATION_START_POWER = 220
# в миллисекундах
CALIBRATION_LEFT_BOUND = 100
CALIBRATION_RIGHT_BOUND = 6000

calibrated_turns : dict[int,  dict[str, int | float]] = dict()

# {
#     "laser": {
#         "1": 65535,
#         "2": 65535,
#         "3": 71,
#         "4": 124,
#         "5": 107,
#         "6": 316G
#     },
#     "imu": {
#         "roll": 1,
#         "pitch": 1,
#         "yaw": 357
#     }
# }

# Информация по датчикам:
#
# 1 датчик смотрит назад
# 2 датчик смотрит влево
# 3 датчик правый под 45 градусов
# 4 датчик передний
# 5 датчик правый
# 6 датчик 45 градусов левый
