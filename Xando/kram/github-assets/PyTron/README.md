# PyTron

### CMPUT 275 Final Project

![PyTron Logo](http://puu.sh/ojnEe/8cfac41538.png "PyTron")

Number of Players: 0-2

## Introduction:

PyTron is a remake of the original Tron light cycles game in python. In PyTron your goal
is to survive the longest as you travel at a constant speed leaving a trail behind you.
If you crash into your own trail, your opponent's trail or a wall you will instantly lose.
This version of the game implements multiple game modes including two player games, player vs bot
games and bot vs bot games. The game also includes win/lose stats for each game mode.

##### Number of Players: 0-2

## Installation instructions:

After Cloning or downloading this repo, with pygame already installed use a terminal or command prompt to navigate to the main directory of this project.
Then type “python3 PyTron.py” to start the game. Use the arrow keys to navigate the main menu.

## Controls:
#### Player 1 (Red):
Action | Key
--- | ---
Up | W
Down | S
Left | A
Right | D

#### Player 2 (Green):
Action | Key
--- | ---
Up | Up Arrow
Down | Down Arrow
Left | Left Arrow
Right | Right Arrow



## A.I. Explanation:

The AI for PyTron is fairly simple. We have two AIs, one random AI and one that considers 'controlled territory'
(default). The random AI will for every tick simply have a 10% chance to chose a new direction. The territory
based AI is slightly more sophisticated and calculates the total number of reachable squares that a player can reach
before all other players for a given direction. For every tick, the territory based AI will consider all possible moves
that it can make assuming the opponent picks a random direction for the next move. The direction which maximizes the
amount of territory is then selected for the next move.


## Acknowledgments:

- This project was inspired by the light cycles minigame in Tron by Bally Midway/Bill Adams.
- This project used pygame as a graphics engine found [here](http://www.pygame.org/hifi.html).

## Authors:
- [nwlieb](https://github.com/nwlieb)
- [eyesniper2](https://github.com/eyesniper2)
