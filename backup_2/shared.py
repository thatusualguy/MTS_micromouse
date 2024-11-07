from backup.Point import Point

# TYPE = "local"
TYPE = "real"


center = [Point(7, 7), Point(7, 8), Point(8, 8), Point(8, 7), ]
graph: dict[Point, list[Point]] = dict()


# robot_ip = "https://"+ "192.168.201.213"
# robot_id = "7536AF1646774A53"

real_baseUrl = "https://"+ "192.168.201.213"
real_robotId = "7536AF1646774A53"
gyro_correction = 0
calibration_filename = 'calibrated_data.json'
real_CELL_SIZE = 180
real_robotSize = 75

local_calibration_filename = 'local_calibrated_data.json'
local_baseUrl = "http://127.0.0.1:8801/api/v1/"
local_token = 'some-token-code'
local_CELL_SIZE = 180
local_robotSize = 75

MOVE_SLEEP_TIME = 0.20
CALIBRATION_EPS = 5
CALIBRATION_COUNT_TESTS = 10
CALIBRATION_STEP = 10
CALIBRATION_START_POWER = 190
# в миллисекундах
CALIBRATION_LEFT_BOUND = 20
CALIBRATION_RIGHT_BOUND = 600


FORWARD_DIST = 160
BACK_DIST = 40
# 150
# 105
# 70

MOVE_SPEED = 70
ROTATE_SPEED = 85

prev_request = -10000
wait_time = 0.1


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
# 6 датчик влево
# 5 датчик влево под 45
# 4 вперёд
# 3 вправо 45
# 2 вправо
# 1 назад

