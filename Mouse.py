from  math import cos, sin, radians

from MouseCommand import *
from Point import *


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
        MouseCommands.forward_one()

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
