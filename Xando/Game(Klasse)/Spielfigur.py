import pygame

import Spielfeld

def erfrage(event, x, y):
    if event.key == pygame.K_w:
        y = y - 1
    elif event.key == pygame.K_s:
        y = y + 1
    elif event.key == pygame.K_a:
        x = x - 1
    elif event.key == pygame.K_d:
        x = x + 1

    return x, y

def bewege(mySpielfeld, x, y, event):
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "0")
    (x, y) = erfrage(event, x, y)
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "X")
    Spielfeld.ausgabe(mySpielfeld)

    return mySpielfeld, x, y