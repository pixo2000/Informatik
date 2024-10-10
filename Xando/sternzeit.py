# 1000 sartada units = 1 earth year
# n = anzahl der tage im jahr also 365 bzw 366 für schaltjahre
# b = das jahr in der berechnung anfängt(2005 = 58000.00/2323 = 00000.00)
# c = die sternzeit zum jahr 'b'
# m = nummer der tage vom monat: Januar = 0, Februar = 31(bei allen weiteren +1 rechnen wenn es ein schaltjahr ist)
#     März = 59, April = 90, Mai = 120, Juni = 151, Juli = 181, August = 212, September = 243, Oktober = 273,
#     November = 304, Dezember = 334
# d = tag im monat
# y = jahr
#
# Beispiel: 23. Mai 2008 wird zu -> n = 366; b = 2005; c = 58000.00; m = 121 (120, +1 wegen Schaltjahr); d = 23; y = 2008. 
#
# Formel: c + (1000*(y-b)) + ((1000/n)*(m + d -1))
# Sternzeit immer 2 nachkommastellen
#

# s = schaltjahrnummer
# s2 = für monat ob +1 sein soll
# https://www.wikihow.com/Calculate-Stardates

b = input("Wann fängt die rechnung an? 2005/2323?: ")
m = input("Welchen Monat haben wir?: ")
d = input("Welchen Tag haben wir?: ")
y = input("Welches Jahr haben wir?: ")

if 


if m = "Januar":
    m = 0
if m = "Februar":
    m= 31
if m = "März":
    m = 59 + s


# Schaltjahrrechnung
while y > 4:
    y - 4
    s + 1
    if y < 4:


# jahr 2008 war schaltjahr.
# beispiel 2034:
# 2034, 2030, 2026, 2022, 2018, 2014, 2010

# immer zieljahr minus erstes schaltjahr und dann berechnung sonst kommt zu viel raus

# für s2 checken ob generell was übrig bleibt und wenn ja auf true setzen zum späteren abfragen

# wann startet der aktuelle kalender
# genauere schaltjahre(nicht nur alle 4 jahre sondern auch alle 100 ig)