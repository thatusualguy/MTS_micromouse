from hand_rule_solve import *
import logging


def run_by_history():
    logging.info('start run by history')
    robot = AA(isRightHand=True)
    filename = input('get filename of history: ')

    if filename == "":
        filename = "test_labirint.json"

    robot.load_history(filename)
    logging.info(f'{filename} is readed, lets start')
    skip = input('How much to skip? ')

    if skip == "":
        skip = 0
    else:
        skip = int(skip)

    start = input('Start?')
    logging.info('run by history')
    robot.run_by_history(skip)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    run_by_history()
