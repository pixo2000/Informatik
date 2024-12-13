import keyboard
from logging_functions import log

def print_game(game):
    log.info("Printing game")
    for line in game:
        print(line)

def create_game_area(height, width):
    log.info("Creating game area with height: %s, width: %s", height, width)
    result = []

    for line in range(height):
        result += ["0" * width]

    return result

def read_coords(game ,x, y):
    log.info("Reading coordinates x: %s, y: %s", x, y)
    line = game[y]

    return line[x]

def write_coords(game, x, y, symbol):
    log.info("Writing symbol %s to coordinates x: %s, y: %s", symbol, x, y)
    result = game.copy()

    line = result[y]

    result[y] = line[:x] + symbol + line[x + 1:]

    return result

def check_player_coords(game):
    log.info("Checking player coordinates")
    for y, line in enumerate(game):
        for x, symbol in enumerate(line):
            if symbol == "X":
                return (x, y)

    return None