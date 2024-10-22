from  math import *

from Mouse import Mouse
from Mover import *
from PathFinder import *
from MouseCommand import *
from Point import *

from shared import graph

class Mapper:

    @staticmethod
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

    @staticmethod
    def has_direct_connection_to(mouse: Mouse) -> list[Point]:
        sensors: dict[int, int] = Mapper.sensors_to_blocks(MouseCommands.sensors())
        res = []

        for heading, dist in sensors.items():
            if dist == 0:
                continue

            heading = mouse.to_global_heading(heading)
            cur = mouse.pos
            dx = - round(1 *cos(radians(heading)))
            dy = round(1 * sin(radians(heading)))
            res.append(Point(cur.x + dx, cur.y + dy))

        return res

    @staticmethod
    def dfs_map():

        visited_total = 0

        mouse = Mouse.Mouse()

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
            how = PathFinder.dijkstra_basic_find_way_to(graph, mouse.pos.clone(), cur.clone())
            if len(how) > 2:
                print("Moving too far! ", len(how), " nodes")
            Mover.basic_follow_path(mouse, how)

            if cur not in visited:
                visited.append(cur.clone())
                visited_total += 1

            # if visited_total > 70:
            #     stack.clear()
            #     continue

            neighbors = Mapper.has_direct_connection_to(mouse)
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
