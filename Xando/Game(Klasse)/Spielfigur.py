import pygame

import Spielfeld

def erfrage(event, x, y, spielfeld):
    hoehe = len(spielfeld)
    breite = len(spielfeld[0])

    if event.key == pygame.K_w and y > 0:
        y = y - 1
    elif event.key == pygame.K_s and y < hoehe - 1:
        y = y + 1
    elif event.key == pygame.K_a and x > 0:
        x = x - 1
    elif event.key == pygame.K_d and x < breite - 1:
        x = x + 1

    return x, y

def bewege(mySpielfeld, x, y, event):
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "0")
    (x, y) = erfrage(event, x, y, mySpielfeld)
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "X")
    # Spielfeld.ausgabe(mySpielfeld)

    return mySpielfeld, x, y