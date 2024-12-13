import random

def verteile_erze(spielfeld, anzahl_gold, anzahl_silber, anzahl_platin):
    for _ in range(anzahl_gold):
        platziere_erz(spielfeld, "G")
    for _ in range(anzahl_silber):
        platziere_erz(spielfeld, "S")
    for _ in range(anzahl_platin):
        platziere_erz(spielfeld, "P")
    return spielfeld

def platziere_erz(spielfeld, erz):
    while True:
        x = random.randint(0, len(spielfeld) - 1)
        y = random.randint(0, len(spielfeld[0]) - 1)
        if spielfeld[x][y] == " ":
            spielfeld[x][y] = erz
            break

def sammle_erz(spielfeld, x, y, gesammelte_erze):
    if spielfeld[x][y] in ["G", "S", "P"]:
        gesammelte_erze[spielfeld[x][y]] += 1
        spielfeld[x][y] = " "
    return gesammelte_erze