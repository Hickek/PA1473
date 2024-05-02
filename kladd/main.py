#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button, Color
from pybricks.tools import wait

# Initialize EV3 brick
ev3 = EV3Brick()

# Define menu options
menu_options = ["Option 1", "Option 2", "Option 3"]
selected_option = 0

# Function to display menu
def display_menu():
    ev3.screen.clear()
    for idx, option in enumerate(menu_options):
        if idx == selected_option:
            ev3.screen.draw_text(10, 20 * idx, "-> " + option)
        else:
            ev3.screen.draw_text(10, 20 * idx, option)
    #ev3.screen.update()

# Main loop
while True:
    display_menu()

    # Wait for button press
    while not any(ev3.buttons.pressed()):
        wait(10)

    # Handle button press
    if Button.UP in ev3.buttons.pressed():
        selected_option = (selected_option - 1) % len(menu_options)
    elif Button.DOWN in ev3.buttons.pressed():
        selected_option = (selected_option + 1) % len(menu_options)
    elif Button.CENTER in ev3.buttons.pressed():
        # Do something when the center button is pressed
        selected_option_text = menu_options[selected_option]
        print("Selected:", selected_option_text)
        # Add your code here for what you want to do with the selected option
