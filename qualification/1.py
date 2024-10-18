import copy
import heapq
import subprocess
import sys
import math
import time
import typing

import pkg_resources

required = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print('installing missing', *missing)
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing])
else:
    print('no packages installed')

import requests

baseUrl = "http://127.0.0.1:8801/api/v1/"

token = "b4e1d501-d270-4ead-ab3c-111c5c25338651365c0e-48ec-4289-a8ad-9864f9bfefdd"
last_request_timestamp = -10000
cooldown_time = 0.200


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


def get_time():
    return time.time()


class Move(object):
    _base = "robot-cells"
    _forward = "forward"
    _backwards = "backward"
    _right = "right"
    _left = "left"

    @staticmethod
    def move(direction):
        global last_request_timestamp
        url = baseUrl + Move._base + '/' + direction + '?token=' + token

        Move.wait()

        requests.post(url).json()
        pass

    @staticmethod
    def wait():
        global last_request_timestamp
        if (last_request_timestamp + cooldown_time) > get_time():
            sleep_time = last_request_timestamp + cooldown_time - get_time()
            time.sleep(sleep_time)
        last_request_timestamp = get_time()

    @staticmethod
    def forward():
        Move.move(Move._forward)

    @staticmethod
    def turn_right():
        Move.move(Move._right)

    @staticmethod
    def turn_left():
        Move.move(Move._left)

    @staticmethod
    def sensors():
        url = baseUrl + Move._base + '/' + "sensor-data" + '?token=' + token
        Move.wait()
        result = requests.get(url).json()
        # print(result)
        return result


class MazeControl(object):
    _base = "maze"

    @staticmethod
    def restart():
        url = baseUrl + MazeControl._base + '/' + "restart" + '?token=' + token
        print("restart")
        requests.post(url).json()


class Task1(object):
    _base = "matrix"

    @staticmethod
    def send_matrix(matrix: list[list[int]]):
        url = baseUrl + Task1._base + '/' + "send" + '?token=' + token
        print("matrix", requests.post(url, json=matrix).json())


class PositionHandler_v2(object):
    pos = Point(15, 0)
    heading: int = 0

    def _normalize(self):
        self.heading = self.heading % 360

    def right(self):
        self.heading += 90
        self._normalize()
        Move.turn_right()

    def left(self):
        self.heading += 270
        self._normalize()
        Move.turn_left()

    def forward(self):
        self.pos.x += - round(1 * math.cos(math.radians(self.heading)))
        self.pos.y += round(1 * math.sin(math.radians(self.heading)))
        Move.forward()

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


def to_blocks(sensor_data):
    values = [
        sensor_data['front_distance'],
        sensor_data['right_side_distance'],
        sensor_data['left_side_distance'],
        sensor_data['back_distance'],
    ]

    values_in_blocks = []
    for value in values:
        if value < 80:
            values_in_blocks.append(0)
            continue
        value = round(value / 160.0)
        values_in_blocks.append(value)

    directions = [
        0, 90, 270, 180
    ]
    return dict(zip(directions, values_in_blocks))


walls_they_want: dict[tuple[bool, bool, bool, bool], int] = {
    # лево верх право низ
    (False, False, False, False): 0,
    (True, False, False, False): 1,
    (False, True, False, False): 2,
    (False, False, True, False): 3,
    (False, False, False, True): 4,
    (True, False, False, True): 5,
    (False, False, True, True): 6,
    (False, True, True, False): 7,
    (True, True, False, False): 8,
    (True, False, True, False): 9,
    (False, True, False, True): 10,
    (False, True, True, True): 11,
    (True, True, True, False): 12,
    (True, True, False, True): 13,
    (True, False, True, True): 14,
    (True, True, True, True): 15,
}


def format_for_send(graph: dict[Point, list[Point]]) -> list[list[int]]:
    size = 16
    result: list[list[int]] = [[0 for col in range(size)] for row in range(size)]

    for vertex, conns in graph.items():

        top = True  # is there a wall?
        right = True
        left = True
        down = True
        for con in conns:
            delta = Point.delta(vertex, con)

            if delta.x != 0:
                if delta.x > 0:
                    top = False
                elif delta.x < 0:
                    down = False
            if delta.y != 0:
                if delta.y < 0:
                    right = False
                elif delta.y > 0:
                    left = False

        result[vertex.x][vertex.y] = walls_they_want[left, top, right, down]

    return result


def maze_mapper_v1():
    need_to_visit = 4 * 4 - 4
    visited_total = 0

    mouse = PositionHandler_v2()

    visited_total += 1

    # Create a stack for DFS
    stack: list[Point] = [mouse.pos]
    visited: list[Point] = []
    graph: dict[Point, list[Point]] = dict()

    def move_to(target: Point):
        nonlocal graph
        nonlocal mouse

        start: Point = mouse.pos.clone()
        if target == start:
            return

        # Initialize distances with infinity and set the distance to the start node to 0
        distances: dict[Point, float] = {node.clone(): float('inf') for node in graph.keys()}
        distances[start.clone()] = 0
        priority_queue: list[tuple[int, Point]] = [(0, start.clone())]  # (distance, node)

        # To save the shortest paths
        shortest_paths = {node: [] for node in graph.keys()}
        shortest_paths[start.clone()] = [start]

        while priority_queue:
            current_distance: int
            current_node: Point
            current_distance, current_node = heapq.heappop(priority_queue, )

            # Nodes can only get added once with their shortest distance
            if current_distance > distances[current_node]:
                continue

            # Iterate over the neighbors of the current node
            for neighbor in graph[current_node]:
                distance = current_distance + 1

                # If a shorter path to the neighbor is found, update the priority queue
                if distance < distances[neighbor.clone()]:
                    distances[neighbor.clone()] = distance
                    heapq.heappush(priority_queue, (distance, neighbor.clone()))
                    # Update the path
                    shortest_paths[neighbor.clone()] = shortest_paths[current_node.clone()] + [neighbor.clone()]

        path = shortest_paths[target]

        path.pop(0)

        while path:
            next: Point = path.pop(0).clone()
            cur = mouse.pos

            dx: int = next.x - cur.x
            if dx != 0:
                if dx < 0:
                    mouse.turn_to(0)
                else:
                    mouse.turn_to(180)
            dy = next.y - cur.y
            if dy != 0:
                if dy > 0:
                    mouse.turn_to(90)
                else:
                    mouse.turn_to(270)
            mouse.forward()

    def has_connection_to(sensors: dict[int, int]) -> list[Point]:
        nonlocal mouse
        res = []
        for hdng, dist in sensors.items():
            if dist == 0:
                continue

            hdng = mouse.to_global_heading(hdng)
            cur = mouse.pos
            dx = - round(1 * math.cos(math.radians(hdng)))
            dy = round(1 * math.sin(math.radians(hdng)))
            res.append(Point(cur.x + dx, cur.y + dy))

        return res

    while len(stack):
        s = stack[-1].clone()
        stack.pop()
        move_to(s.clone())

        if s not in visited:
            visited.append(s.clone())
            visited_total += 1

        # if visited_total > 5:
        #     stack.clear()
        #     continue

        sensors: dict[int, int] = to_blocks(Move.sensors())
        neighbors = has_connection_to(sensors)
        for node in neighbors:
            if node not in visited:
                stack.append(node.clone())

                if s not in graph.keys():
                    graph[s.clone()] = [node.clone()]
                else:
                    graph[s.clone()].append(node.clone())

                if graph.get(node) is None:
                    graph[node.clone()] = [s.clone()]
                else:
                    graph[node.clone()].append(s.clone())

    print(visited_total)
    print(len(visited))
    res = format_for_send(graph)
    Task1.send_matrix(res)
    print(json.dumps(res))


maze_mapper_v1()
