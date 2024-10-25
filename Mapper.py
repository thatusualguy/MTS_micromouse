from  math import *

from Mouse import Mouse
from Mover import *
from PathFinder import *
from MouseCommand import *
from Point import *

from shared import graph

class Mapper:

    @staticmethod
    def has_direct_connection_to(mouse: Mouse) -> list[Point]:
        blocks: dict[int, int] = MouseCommands.sensors_to_blocks()
        res = []

        for heading, blocks in blocks.items():
            if blocks == 0:
                continue

            heading = mouse.to_global_heading(heading)
            cur = mouse.pos
            dx = - round(1 *cos(radians(heading)))
            dy = round(1 * sin(radians(heading)))
            res.append(Point(cur.x + dx, cur.y + dy))

        return res

    @staticmethod
    def dfs_map():
        global graph
        visited_total = 0

        mouse = Mouse.Mouse()

        stack: list[Point] = [mouse.pos]
        visited: list[Point] = []

        while len(stack):
            print("Progress discovering map: ", len(visited), '/', 16 * 16, " = ", int(len(visited) / (16 * 16) * 100),
                  '%', sep='')
            print("Progress map:", *map(str, graph))

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
