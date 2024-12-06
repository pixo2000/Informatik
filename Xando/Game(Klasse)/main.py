import game
import logging_functions as logger
from logging_functions import log


def run_game():
    runningGame = game.create_game_area(10, 5)
    runningGame = game.write_coords(runningGame, 3, 3, "X")
    game.print_game(runningGame)
def main():
    logger.start_logging("DEBUG")
    run_game()
    log.info("Game finished")

if __name__ == '__main__':
    main()