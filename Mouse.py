from  math import cos, sin, radians

from MouseCommand import *
from Point import *



def sensors_to_blocks(sensor_data: dict[str, float]) -> dict[int, int]:
    values = [
        sensor_data['mapper']["1"],
        sensor_data['mapper']["2"],
        sensor_data['mapper']["3"],
        sensor_data['mapper']["4"],
        sensor_data['mapper']["5"],
        sensor_data['mapper']["6"],
    ]

    values_in_blocks = []
    for value in values:
        if value < 80:
            values_in_blocks.append(0)
            continue
        value = round(value / 160.0)
        values_in_blocks.append(value)

    directions = [
        180, 270, 45, 0, 90, 360-45
    ]
    return dict(zip(directions, values_in_blocks))

class Mouse(object):
    pos: Point
    heading: int

    def __init__(self, x=15, y=0, heading=0):
        self.pos = Point(x, y)
        self.heading = heading

    def _normalize(self):
        self.heading = self.heading % 360

    def right(self):
        self.heading += 90
        self._normalize()
        MouseCommands.turn_right_90()

    def left(self):
        self.heading += 270
        self._normalize()
        MouseCommands.turn_left_90()

    def forward(self):
        self.pos.x += - round(1 * cos(radians(self.heading)))
        self.pos.y += round(1 * sin(radians(self.heading)))
        MouseCommands.forward(165)

    def turn_to(self, new_heading: int):
        while new_heading != self.heading:
            turn_deg = new_heading - self.heading

            if turn_deg > 180:
                turn_deg -= 360
            elif turn_deg < -180:
                turn_deg += 360

            if turn_deg == 0:
                return
            elif turn_deg < 0:
                self.left()
            elif turn_deg > 0:
                self.right()

    def to_global_heading(self, direction):
        return (self.heading + direction) % 360

    def __str__(self):
        return str(self.__dict__)
