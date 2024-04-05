#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from pybricks.tools import wait

# Initialize the EV3 Brick
ev3 = EV3Brick()

def main_menu():
    menu_items = ["Pick Up", "Drop Off", "Detect Color", "Exit"]
    current_selection = 0  # Start with the first menu item

    while True:
        # Clear the screen and display the current menu item
        ev3.screen.clear()
        for i, item in enumerate(menu_items):
            if i == current_selection:
                ev3.screen.draw_text(10, 20 * i, "> " + item)  # Highlight selected item
            else:
                ev3.screen.draw_text(10, 20 * i, "  " + item)

        # Wait for a button press
        pressed = []
        while not pressed:
            pressed = ev3.buttons.pressed()

        # Update the selection based on the button press
        if Button.DOWN in pressed:
            current_selection = (current_selection + 1) % len(menu_items)
        elif Button.UP in pressed:
            current_selection = (current_selection - 1) % len(menu_items)
        elif Button.CENTER in pressed:
            return menu_items[current_selection]  # Return the selected action

        wait(200)  # Debounce delay

def execute_selection(selection):
    # Placeholder function to execute the selected menu item
    if selection == "Pick Up":
        ev3.screen.clear()
        ev3.screen.draw_text(10, 20, "Picking up...")
        pickuploc = input("Välj ")# Add your pick-up logic here
    elif selection == "Drop Off":
        ev3.screen.clear()
        ev3.screen.draw_text(10, 20, "Dropping off...")
        # Add your drop-off logic here
    elif selection == "Detect Color":
        ev3.screen.clear()
        ev3.screen.draw_text(10, 20, "Detecting color...")
        # Add your color detection logic here
    elif selection == "Exit":
        ev3.screen.clear()
        ev3.screen.draw_text(10, 20, "Exiting...")
        wait(1000)
        ev3.screen.clear()
        exit()

# Main loop
while True:
    selection = main_menu()  # Show the menu and get the selection
    execute_selection(selection)  # Execute the selected action
