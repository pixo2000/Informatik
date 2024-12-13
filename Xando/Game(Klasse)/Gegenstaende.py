import random
import Spielfeld

def platziere_edelmetall(spielfeld, anzahl, symbol):
    hoehe = len(spielfeld)
    breite = len(spielfeld[0])

    for i in range(anzahl):
        while True:
            x = random.randint(0, breite - 1)
            y = random.randint(0, hoehe - 1)
            if spielfeld[y][x] == '0':
                spielfeld = Spielfeld.schreibe(spielfeld, x, y, symbol)
                break

    return spielfeld


def platziere_gold(spielfeld, anzahl):
    return platziere_edelmetall(spielfeld, anzahl, 'G')


def platziere_silber(spielfeld, anzahl):
    return platziere_edelmetall(spielfeld, anzahl, 'S')


def platziere_platin(spielfeld, anzahl):
    return platziere_edelmetall(spielfeld, anzahl, 'P')