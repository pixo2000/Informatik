import game

runningGame = game.create_game_area(10, 10)

game.print_game(runningGame)

coords = (3, 3)
game.write_coords(runningGame, coords[0], coords[1], "X")

false = True

while false:
    movement = input("Enter a direction: ")
    game.write_coords(runningGame, coords[0], coords[1], "0")

    if movement == "up":
        coords[2] = coords[2] - 1

    elif movement == "down":
        coords[2] = coords[2] + 1

    elif movement == "left":
        coords[1] = coords[1] - 1

    elif movement == "right":
        coords[1] = coords[1] + 1

runningGame = game.write_coords(runningGame, coords[0], coords[1], "X")
game.print_game(runningGame)

# wo setzt er coords auf 0?!?
