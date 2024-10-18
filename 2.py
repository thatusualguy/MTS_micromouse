import copy
import heapq
import math
import time
import typing

import sys
import subprocess
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


class MouseCommands(object):
    _base = "robot-cells"
    _forward = "forward"
    _backwards = "backward"
    _right = "right"
    _left = "left"

    @staticmethod
    def move(direction):
        global last_request_timestamp
        url = baseUrl + MouseCommands._base + '/' + direction + '?token=' + token

        MouseCommands.wait()
        requests.post(url).json()

    @staticmethod
    def wait():
        global last_request_timestamp
        if (last_request_timestamp + cooldown_time) > get_time():
            sleep_time = last_request_timestamp + cooldown_time - get_time()
            time.sleep(sleep_time)
        last_request_timestamp = get_time()

    @staticmethod
    def forward():
        MouseCommands.move(MouseCommands._forward)

    @staticmethod
    def turn_right():
        MouseCommands.move(MouseCommands._right)

    @staticmethod
    def turn_left():
        MouseCommands.move(MouseCommands._left)

    @staticmethod
    def sensors():
        url = baseUrl + MouseCommands._base + '/' + "sensor-data" + '?token=' + token
        MouseCommands.wait()
        return requests.get(url).json()


class MazeControl(object):
    _base = "maze"

    @staticmethod
    def restart():
        url = baseUrl + MazeControl._base + '/' + "restart" + '?token=' + token
        print("restart")
        requests.post(url).json()


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
        MouseCommands.turn_right()

    def left(self):
        self.heading += 270
        self._normalize()
        MouseCommands.turn_left()

    def forward(self):
        self.pos.x += - round(1 * math.cos(math.radians(self.heading)))
        self.pos.y += round(1 * math.sin(math.radians(self.heading)))
        MouseCommands.forward()

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


graph: dict[Point, list[Point]] = dict()
center = [Point(7, 7), Point(7, 8), Point(8, 8), Point(8, 7), ]


class Solve:

    @staticmethod
    def dijkstra_basic_find_way_to(graph: dict[Point, list[Point]], start: Point, target: Point) -> list[Point]:
        if target == start:
            return []

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
        return path


class Move:
    @staticmethod
    def basic_follow_path(mouse: Mouse, path: list[Point], end_in_center=False):
        global center

        while path:
            target: Point = path.pop(0).clone()
            cur = mouse.pos

            if end_in_center:
                if cur in center:
                    return

            dx: int = target.x - cur.x
            if dx != 0:
                if dx < 0:
                    mouse.turn_to(0)
                else:
                    mouse.turn_to(180)
            dy = target.y - cur.y
            if dy != 0:
                if dy > 0:
                    mouse.turn_to(90)
                else:
                    mouse.turn_to(270)
            mouse.forward()


class Mapp:

    @staticmethod
    def sensors_to_blocks(sensor_data: dict[str, float]) -> dict[int, int]:
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

    @staticmethod
    def has_direct_connection_to(mouse: Mouse) -> list[Point]:
        sensors: dict[int, int] = Mapp.sensors_to_blocks(MouseCommands.sensors())
        res = []

        for heading, dist in sensors.items():
            if dist == 0:
                continue

            heading = mouse.to_global_heading(heading)
            cur = mouse.pos
            dx = - round(1 * math.cos(math.radians(heading)))
            dy = round(1 * math.sin(math.radians(heading)))
            res.append(Point(cur.x + dx, cur.y + dy))

        return res

    @staticmethod
    def dfs_map():
        global graph
        global center

        visited_total = 0

        mouse = Mouse()

        stack: list[Point] = [mouse.pos]
        visited: list[Point] = []

        while len(stack):
            print("Progress discovering map: ", len(visited), '/', 16 * 16, " = ", int(len(visited) / (16 * 16) * 100),
                  '%', sep='')

            cur = stack[-1].clone()
            stack.pop()

            if cur in center:
                print("Found center!")
                visited.append(cur)
                continue

            # move to new node
            how = Solve.dijkstra_basic_find_way_to(graph, mouse.pos.clone(), cur.clone())
            if len(how) > 2:
                print("Moving too far! ", len(how), " nodes")
            Move.basic_follow_path(mouse, how)

            if cur not in visited:
                visited.append(cur.clone())
                visited_total += 1

            # if visited_total > 5:
            #     stack.clear()
            #     continue

            neighbors = Mapp.has_direct_connection_to(mouse)
            for node in neighbors:
                if node not in visited:
                    stack.append(node.clone())

                    if cur not in graph.keys():
                        graph[cur.clone()] = [node.clone()]
                    else:
                        graph[cur.clone()].append(node.clone())

                    if graph.get(node) is None:
                        graph[node.clone()] = [cur.clone()]
                    else:
                        graph[node.clone()].append(cur.clone())

        return graph


# map full map
full_graph = Mapp.dfs_map()
print("Found map:", *map(str, full_graph))
print("Nodes:", len(full_graph))

path = Solve.dijkstra_basic_find_way_to(full_graph, Point(15, 0), Point(7, 7))
print("Found path:", *map(str, path))
print("Length:", len(path))

MazeControl.restart()
time.sleep(2)

print("First run")
# run best line twice
cooldown_time = 0.150
Move.basic_follow_path(Mouse(), path, end_in_center=True)
time.sleep(0.5)
MazeControl.restart()

print("Second run")
# lower cooldown for a try
# noinspection PyRedeclaration
cooldown_time = 0.130
Move.basic_follow_path(Mouse(), path, end_in_center=True)
time.sleep(0.5)
MazeControl.restart()
