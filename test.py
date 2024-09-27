benutzereingabe = input("Bitte Namen eingeben: ")

# man kann auch nach typen filtern aber das zu aufwändig
if (type(benutzereingabe) == str):
     if (benutzereingabe == "exit"):
           print("Exiting cuz u typed exit")
           quit()
     else:
           print("Hallo: " + benutzereingabe)
           quit()
else:
     print("Error. No String")