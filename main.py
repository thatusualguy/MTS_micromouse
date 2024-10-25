from Mouse import Mouse
from Mapper import Mapper
from Mover import Mover
from PathFinder import PathFinder
from MouseCommand import MouseCommands
from Point import Point

input("Готов к забегу - исследованию?")

MouseCommands.calibrate_gyro()

# map full map
full_graph = Mapper.dfs_map()
print("Found map:", *map(str, full_graph))
print("Nodes:", len(full_graph))

path = PathFinder.dijkstra_basic_find_way_to(full_graph, Point(15, 0), Point(7, 7))
print("Found path:", *map(str, path))
print("Found path:", *map(lambda x: x.to_array(), path))
print("Length:", len(path))


input("Готов к забегу - на время 1?")
MouseCommands.calibrate_gyro()
Mover.basic_follow_path(Mouse(), path, end_in_center=True)
print("Конец забега")


input("Готов к забегу - на время 2?")
MouseCommands.calibrate_gyro()
Mover.basic_follow_path(Mouse(), path, end_in_center=True)
print("Конец")
