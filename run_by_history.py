from hand_rule_solve import *
import logging


def main():
    logging.info('start run by history')
    robot = AA(isRightHand=True)
    filename = input('get filename of history: ')
    robot.load_history(filename)
    logging.info('f{filename} is readed, lets start')
    start = input('Start?')
    logging.info('run by history')
    # robot.run_by_history()


if __name__ == "__main__":
    main()
