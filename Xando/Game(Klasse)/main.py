import game
import logging_functions as logger
from logging_functions import log


def run_game():
    # set startcoords here
    startcoords = (3, 3)
    runningGame = game.create_game_area(10, 5)
    runningGame = game.write_coords(runningGame, startcoords[0], startcoords[1], "X")
    game.print_game(runningGame)
    game.control(runningGame)

def main():
    logger.start_logging("DEBUG")
    run_game()
    log.info("Game finished")

if __name__ == '__main__':
    main()