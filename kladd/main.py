#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from pybricks.tools import wait

# Initialize EV3 brick
ev3 = EV3Brick()

# Define menu options
menu_options = ["Emergency", "Pause", "Schedule"]
selected_option = 0
paused = False

# Function to display menu
def display_menu():
    ev3.screen.clear()
    for idx, option in enumerate(menu_options):
        if idx == selected_option:
            ev3.screen.draw_text(10, 10 * idx, " --> " + option)
        else:
            ev3.screen.draw_text(10, 10 * idx, option)

# Main loop
while True:
    display_menu()

    # Wait for button press
    while not any(ev3.buttons.pressed()):
        wait(10)

    # Handle button press
    wait(200)  # Debounce delay
    if Button.UP in ev3.buttons.pressed():
        selected_option = (selected_option - 1) % len(menu_options)
    elif Button.DOWN in ev3.buttons.pressed():
        selected_option = (selected_option + 1) % len(menu_options)
    elif Button.CENTER in ev3.buttons.pressed():
        # Do something when the center button is pressed
        if selected_option == 0:
            ev3.screen.clear()
            ev3.screen.draw_text(10, 10, "Shutting Down")
            wait(3000)
        elif selected_option == 1:
            paused = not paused
            if paused == True:
                menu_options[1] = "Resume"
            else:
                menu_options[1] = "Pause"
            #pause
        elif selected_option == 2:
            wait(3000)
            
        