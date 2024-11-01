def ist_schaltjahr(jahr):
    return jahr % 4 == 0 and (jahr % 100 != 0 or jahr % 400 == 0)

def tage_im_monat(monat, jahr):
    if monat == 2:
        return 29 if ist_schaltjahr(jahr) else 28
    elif monat in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def erster_wochentag_im_monat(monat, jahr):
    # Zeller's Congruence Algorithm to find the day of the week
    if monat < 3:
        monat += 12
        jahr -= 1
    k = jahr % 100
    j = jahr // 100
    f = 1 + (13 * (monat + 1)) // 5 + k + k // 4 + j // 4 + 5 * j
    return (f % 7 + 5) % 7  # Adjusting to make Monday = 0

def kalender(monat, jahr):
    monthdays = tage_im_monat(monat, jahr)
    start_day = erster_wochentag_im_monat(monat, jahr)
    
    print(f"{monat}/{jahr}")
    print("Mo Di Mi Do Fr Sa So")
    
    # Print leading spaces for the first week
    print("   " * start_day, end="")
    
    day = 1
    while day <= monthdays:
        for _ in range(start_day, 7):
            if day > monthdays:
                break
            print(f"{day:2} ", end="")
            day += 1
        print()
        start_day = 0

# Eingabe von Monat und Jahr über die Konsole
monat = int(input("Bitte geben Sie den Monat ein (1-12): "))
jahr = int(input("Bitte geben Sie das Jahr ein: "))

kalender(monat, jahr)