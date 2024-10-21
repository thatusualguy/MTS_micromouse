from MazeControl import MazeControl
from Mouse import Mouse
from Mapper import Mapper
from Mover import Mover
from PathFinder import *
from MouseCommand import *
from Point import *





# map full map
full_graph = Mapper.dfs_map()
print("Found map:", *map(str, full_graph))
print("Nodes:", len(full_graph))

path = PathFinder.dijkstra_basic_find_way_to(full_graph, Point(15, 0), Point(7, 7))
print("Found path:", *map(str, path))
print("Found path:", *map(lambda x: x.to_array(), path))
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
