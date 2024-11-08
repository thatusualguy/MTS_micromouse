from turn import turn
from move import forward 


def move_forward():
    print('move_forward')
    forward(1) 

def move_backward():
    print('dont work move_backward')

def turn_right():
    print('turn_right')
    turn(90)

def turn_left():
    print('turn_left')
    turn(-90)

def rotate_45_left():
    print('rotate_45_left')
    turn(45)

def rotate_45_right():
    print('rotate_46_right')
    turn(-45)

def rotate_15_left():
    print('rotate_15_left')
    turn(15)

def rotate_15_right():
    print('rotate_15_right')
    turn(-15)

def main():
    input('start_hand_solve?')
    while True:
        command = input()
        if command == 'exit':
            break
        if command == 'w':
            move_forward()
        if command == 's':
            move_backward()
        if command == 'd':
            turn_right()
        if command == 'a':
            turn_left()
        if command == 'q':
            rotate_45_left()
        if command == 'e':
            rotate_45_right()
        if command == '1':
            rotate_15_left()
        if command == '3':
            rotate_15_right()


if __name__ == '__main__':
    main()

