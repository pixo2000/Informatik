# Aufgabe 1:
# Auflistung mit Sternen

# Aufgabe 2:
# als Pyramide

# Aufgabe 3:
# Kreis mit Sternen

import math

# Aufgabe 1:
def aufgabe1(stars):
    result = ""
    count = 1

    while count <= stars:
        result += "*" * count + "\n"
        count += 1

    return result

# Aufgabe 2:
def aufgabe2(stars):
    result = ""
    count = 1

    while count <= stars:
        result += " " * (stars - count) + "*" * (2 * count - 1) + "\n"
        count += 1

    return result

# Aufgabe 3:
def aufgabe3(stars):
    result = ""
    i = 0

    while i < (2 * stars) + 1:
        j = 0
        line = ""
        while j < (2 * stars) + 1:
            if math.sqrt((i - stars) ** 2 + (j - stars) ** 2) <= stars:
                line += "*"
            else:
                line += " "
            j += 1
        result += line + "\n"
        i += 1

    return result

def main():
    try:
        stars = int(input("Bitte gib die Anzahl der Sterne ein: "))
        if stars < 1:
            print("Fehler: Bitte gib eine Zahl größer als 0 ein, um einen Output zu bekommen")
            return

        task = int(input("Bitte gib die Aufgabe ein (1, 2 oder 3): "))
        if task == 1:
            output = aufgabe1(stars)
        elif task == 2:
            output = aufgabe2(stars)
        elif task == 3:
            output = aufgabe3(stars)
        else:
            print("Fehler: Bitte gib eine gültige Aufgabe (1, 2 oder 3) ein.")
            return

        print(output)
    except ValueError:
        print("Fehler: Bitte geben Sie gültige Zahlen ein.")

if __name__ == "__main__":
    main()