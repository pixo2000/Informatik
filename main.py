import time
import keyboard

# um den code immer abbrechen zu können
while not keyboard.is_pressed('p'):
    try:
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
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        quit()
print("Ending Code")