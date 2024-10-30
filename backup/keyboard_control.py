from MouseCommand import MouseCommands

if __name__ == "__main__":

    MouseCommands.calibrate_gyro()
    MouseCommands.calibrate_basic_rotations()
    MouseCommands.load_calibrated_data()
    while True:
        MouseCommands.sensors_raw()
        print("Ожидаю команды... A - налево, D - направо, W - вперед, C - выравнивание")
        cmd = str.lower(input())
        if cmd == "a":
            MouseCommands.turn_left_90()
        if cmd == "d":
            MouseCommands.turn_right_90()
        if cmd == "w":
            MouseCommands.forward_one()
        if cmd == "c":
            MouseCommands.center()
        if cmd == "s":
            print(MouseCommands.sensors())