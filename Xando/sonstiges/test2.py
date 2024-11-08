import math

# Benutzer nach dem Radius fragen
radius = int(input("Bitte geben Sie den Radius des Kreises ein: "))

# Zeichne den gefüllten Kreis
for y in range(-radius, radius + 1):
    for x in range(-radius, radius + 1):
        # Prüfe, ob der Punkt (x, y) innerhalb des Kreises liegt
        if x**2 + y**2 <= radius**2:
            print("* ", end="")
        else:
            print("  ", end="")
    print()
