from MazeControl import MazeControl
from Mouse import *
from Mapper import *
from Mover import *
from PathFinder import *
from MouseCommand import *
from Point import *

baseUrl = "http://127.0.0.1:8801/api/v1/"
token = "b4e1d501-d270-4ead-ab3c-111c5c25338651365c0e-48ec-4289-a8ad-9864f9bfefdd"


graph: dict[Point, list[Point]] = dict()
center = [Point(7, 7), Point(7, 8), Point(8, 8), Point(8, 7), ]


# map full map
full_graph = Mapper.dfs_map()
print("Found map:", *map(str, full_graph))
print("Nodes:", len(full_graph))

path = PathFinder.dijkstra_basic_find_way_to(full_graph, Point(15, 0), Point(7, 7))
print("Found path:", *map(str, path))
print("Length:", len(path))

MazeControl.restart()
time.sleep(2)

print("First run")
# run best line twice
cooldown_time = 0.150
Mover.basic_follow_path(Mouse(), path, end_in_center=True)
time.sleep(0.5)
# MazeControl.restart()

print("Second run")
# lower cooldown for a try
# noinspection PyRedeclaration
cooldown_time = 0.130
Mover.basic_follow_path(Mouse(), path, end_in_center=True)
time.sleep(0.5)
MazeControl.restart()
