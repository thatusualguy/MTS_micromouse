from MouseCommand import MouseCommands




def calibrate_move(dist):

    MouseCommands.back_real(300)

    forward = MouseCommands.sensors()['dist'][0]

    if dist > forward-10:
        print("Can't calibrate",dist, ". too close", forward)
        return

    MouseCommands.forward_real(dist)
    forward_after = MouseCommands.sensors()['dist'][0]
    diff =   forward - forward_after
    print('Expected', forward - dist, " Actual", diff)

def calibrate_input():
    while True:
        dist = int(input("Enter distance: "))
        calibrate_move(dist)

def calibrate_default():
    to_calibrate = [180, 90, 45, 20, 10, 5]
    for dist in to_calibrate:
        calibrate_move(dist)

calibrate_input()