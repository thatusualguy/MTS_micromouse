import copy


class Point(object):
    x: int = 0
    y: int = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + '-' + str(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __hash__(self):
        return hash(self.x * 1000 + self.y)

    def clone(self):
        return copy.deepcopy(self)

    @staticmethod
    def delta(foo, bar):
        return Point(foo.x - bar.x, foo.y - bar.y)
