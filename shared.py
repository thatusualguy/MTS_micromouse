from Point import Point

baseUrl = "http://127.0.0.1:8801/api/v1/"
token = "b4e1d501-d270-4ead-ab3c-111c5c25338651365c0e-48ec-4289-a8ad-9864f9bfefdd"
center = [Point(7, 7), Point(7, 8), Point(8, 8), Point(8, 7), ]
graph: dict[Point, list[Point]] = dict()
