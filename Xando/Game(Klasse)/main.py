import Spielfeld
import Spielfigur
from Gegenstaende import platziere_gold, platziere_silber, platziere_platin


def run_game():
    x = 0
    y = 0

    mySpielfeld = Spielfeld.erzeuge(10, 10)
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "X")
    Spielfeld.ausgabe(mySpielfeld)

    # Place items on the game field
    mySpielfeld = platziere_gold(mySpielfeld, 5)
    mySpielfeld = platziere_silber(mySpielfeld, 3)
    mySpielfeld = platziere_platin(mySpielfeld, 2)

    while True:
        (mySpielfeld, x, y) = Spielfigur.bewege(mySpielfeld, x, y)
        Spielfeld.ausgabe(mySpielfeld)


def main():
    run_game()


if __name__ == '__main__':
    main()