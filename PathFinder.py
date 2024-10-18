import heapq

from Mouse import *
from Mover import *
from MouseCommand import *
from Point import *

class PathFinder:

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
