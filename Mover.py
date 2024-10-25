import Mouse
import Point
from shared import center, graph


class Mover:
    @staticmethod
    def basic_follow_path(mouse: Mouse, path: list[Point], end_in_center=False):

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
