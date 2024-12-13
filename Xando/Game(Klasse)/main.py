import Spielfeld
import Spielfigur


def run_game():
    x = 0
    y = 0

    mySpielfeld = Spielfeld.erzeuge(10, 10)
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "X")
    Spielfeld.ausgabe(mySpielfeld)

    while True:
        (mySpielfeld, x, y) = Spielfigur.bewege(mySpielfeld, x, y)
        Spielfeld.ausgabe(mySpielfeld)


def main():
    run_game()


if __name__ == '__main__':
    main()