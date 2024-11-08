def get_turn_direction(start, target):
    turn = (target - start) % 360
    if turn > 180:
        turn -= 360
    return int(turn)


def closest_angle(angle):
    return  (angle+45)//90* 90 % 360