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

def move_player(game, direction): # bug when moving down
    log.info("Moving player in direction %s", direction)
    coords = check_player_coords(game)

    if direction == "up":
        new_coords = (coords[0], coords[1] - 1)
    elif direction == "down":
        new_coords = (coords[0], coords[1] + 1)
    elif direction == "left":
        new_coords = (coords[0] - 1, coords[1])
    elif direction == "right":
        new_coords = (coords[0] + 1, coords[1])
    else:
        log.error("Invalid direction %s", direction)
        return game

    if new_coords[0] < 0 or new_coords[0] >= len(game[0]) or new_coords[1] < 0 or new_coords[1] >= len(game):
        log.error("Invalid coordinates %s", new_coords)
        return game

    if read_coords(game, new_coords[0], new_coords[1]) == "1":
        log.error("Invalid coordinates %s", new_coords)
        return game

    game = write_coords(game, coords[0], coords[1], "0")
    game = write_coords(game, new_coords[0], new_coords[1], "X")

    return game

def control(game):
    log.info("Starting control loop")
    while True:
        if keyboard.is_pressed("w"):
            game = move_player(game, "up")
            print_game(game)
            print("")
        elif keyboard.is_pressed("s"):
            game = move_player(game, "down")
            print_game(game)
            print("")
        elif keyboard.is_pressed("a"):
            game = move_player(game, "left")
            print_game(game)
            print("")
        elif keyboard.is_pressed("d"):
            game = move_player(game, "right")
            print_game(game)
            print("")
        elif keyboard.is_pressed("esc"):
            break

    return game