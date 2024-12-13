def ausgabe(spielfeld):
    for zeile in spielfeld:
        print(zeile)

def erzeuge(breite, hoehe):
    result = []

    for zeile in range(hoehe):
        result += ["0" * breite]

    return result

def lies(spielfeld ,x, y):
    zeile = spielfeld[y]

    return zeile[x]

def schreibe(spielfeld, x, y, symbol):
    result = spielfeld.copy()

    zeile = result[y]

    result[y] = zeile[:x] + symbol + zeile[x + 1:]

    return result
