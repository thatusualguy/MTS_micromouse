from Point import Point

baseUrl = " http://192.168.68.167/"
robot_id = "854CAF96103A6853"
center = [Point(7, 7), Point(7, 8), Point(8, 8), Point(8, 7), ]
graph: dict[Point, list[Point]] = dict()
gyro_correction = 0

# {
#     "laser": {
#         "1": 65535,
#         "2": 65535,
#         "3": 71,
#         "4": 124,
#         "5": 107,
#         "6": 316
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
