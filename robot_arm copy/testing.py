#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
from pybricks.tools import wait

# Initiera EV3 Brick.
ev3 = EV3Brick()

# Funktion för att visa meny och hantera användarinteraktion.
def display_menu():
    current_selection = 0
    menu_items = ["Paus", "Settings", "Pickup Loc"]
    line_height = 15  # Håll en standardhöjd för linjer för att förbättra läsbarheten

    while True:
        try:
            # Rensa skärmen och visa det nuvarande menyvalet.
            ev3.screen.clear()
            for i, item in enumerate(menu_items):
                y_position = 10 + i * line_height  # Beräkna y-position för varje menyval
                if i == current_selection:
                    ev3.screen.draw_text(5, y_position, "-> " + item)
                else:
                    ev3.screen.draw_text(5, y_position, "   " + item)

            while True:
                button_pressed = ev3.buttons.pressed()
                if button_pressed:
                    break  # Bryt loopen om en knapp är nedtryckt

            # Navigera i menyn eller välj ett alternativ.
            if Button.UP in ev3.buttons.pressed():
                current_selection = (current_selection - 1) % len(menu_items)
            elif Button.DOWN in ev3.buttons.pressed():
                current_selection = (current_selection + 1) % len(menu_items)
            elif Button.CENTER in ev3.buttons.pressed():
                selected_option = handle_selection(menu_items[current_selection])
                if selected_option is not None:
                    return selected_option

        except Exception as e:
            display_error(str(e))

# Hanterar val beroende på användarens val i menyn.
def handle_selection(choice):
    ev3.screen.clear()
    if choice == "Paus":
        ev3.screen.draw_text(5, 30, "System is paused")
        wait(2000)  # Visa detta skärm i 2 sekunder
    elif choice == "Settings":
        ev3.screen.draw_text(5, 30, "Setting Menu")
        wait(2000)  # Visa detta skärm i 2 sekunder
    elif choice == "Pickup Loc":
        ev3.screen.draw_text(5, 30, "Press a button to select pickup location")
        button_pressed = ev3.buttons.wait()  # Vänta på knapptryckning
        if button_pressed in [Button.UP, Button.DOWN, Button.LEFT, Button.RIGHT]:
            return button_pressed  # Returnera knapptrycket

def display_error(message):
    ev3.screen.clear()
    ev3.screen.draw_text(5, 30, "Error:")
    ev3.screen.draw_text(5, 45, message)
    wait(5000)  # Visa felmeddelandet i 5 sekunder

# Huvudfunktionen som kör programmet.
if __name__ == "__main__":
    selected_option = display_menu()
    ev3.screen.clear()
    ev3.screen.draw_text(5, 30, "Selected option: {}".format(selected_option))
    wait(2000)  # Visa vald alternativ i 2 sekunder
