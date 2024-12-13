import Spielfeld

def erfrageBewegung(x, y):
    bewegungsWunsch = input("Richtung: ")

    if bewegungsWunsch == "W":
        y = y - 1

    if bewegungsWunsch == "S":
        y = y + 1

    if bewegungsWunsch == "A":
        x = x - 1

    if bewegungsWunsch == "D":
        x = x + 1

    return x, y

def bewege(mySpielfeld, x, y):
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "0")
    (x, y) = erfrageBewegung(x, y)
    mySpielfeld = Spielfeld.schreibe(mySpielfeld, x, y, "X")

    return mySpielfeld, x, y