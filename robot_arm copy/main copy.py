#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
import threading
import time

# Initialize the EV3 Brick
ev3 = EV3Brick()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.A)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
#elbow_motor.control.limits(speed=60, acceleration=120)
#base_motor.control.limits(speed=200, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
elbow_sensor = ColorSensor(Port.S2)

# Initialize the elbow. First make it go down for one second.
# Then make it go upwards slowly (15 degrees per second) until
# the Color Sensor detects the white beam. Then reset the motor
# angle to make this the zero point. Finally, hold the motor
# in place so it does not move.

#Variable declaration
belt = False
EMERGENCY_ZONE = 155
ZONE_1 = 5
ZONE_2 = 45
ZONE_3 = 102
ZONE_4 = 155 #Remove before release
ZONE_5 = 205 #pickup

#Threading 1/3
paused = False

def pause():
    global paused
    paused = True

def resume():
    global paused
    paused = False
    if belt == True:
        mbox.send("Continue")

def shutdown():
    global paused
    paused = True
    wait(1000)
    elbow_motor.run_target(20, 30)
    base_motor.run_target(20, EMERGENCY_ZONE)
    elbow_motor.run_until_stalled(-20, duty_limit=-10)
    gripper_motor.run_target(20, -90)

def is_paused():
    return paused

def pause_check():
    while is_paused():
        time.sleep(0.1)
    if belt == True:
        mbox.send("Pause")

#Connect conveyor belt
if belt is True:

    server = BluetoothMailboxServer()
    mbox = TextMailbox('greeting', server)


    # The server must be started before the client!
    ev3.screen.draw_text(10, 20, 'waiting for connection...')
    server.wait_for_connection()
    ev3.screen.clear()
    ev3.screen.draw_text(10, 20, 'connected!')

    # In this program, the server waits for the client to send the first message
    # and then sends a reply.
    mbox.wait()
    ev3.screen.clear()
    ev3.screen.draw_text(10, 20, mbox.read())
    mbox.send("Hej")

elbow_motor.run_time(30, 2000)
#elbow_motor.run(-10)
#while elbow_sensor.reflection() < 28:
#    wait(10)
elbow_motor.run_until_stalled(-10, then=Stop.HOLD, duty_limit=6)
elbow_motor.reset_angle(-15)
elbow_motor.hold()
# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
elbow_motor.run_target(30, 50)
base_motor.run(-60)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

# Initialize the gripper. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
gripper_motor.run_until_stalled(100, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(100, -90)

color_list = []
def color_detection():
    # Color detection v3
    # Shown at demo 1
    # Check resistance when closing claw to check if an item is present
    # Also use resistance to place on elevated positions (when items are stacked)

    rgb = elbow_sensor.rgb()
    R = rgb[0]
    G = rgb[1]
    B = rgb[2]
    if max(rgb) == min(rgb):
        hue = -200
    elif R >= G and R >= B:
        hue = (G - B) / (max(rgb) - min(rgb))
    elif G >= R and G >= B:
        hue = 2 + (B - R) / (max(rgb) - min(rgb))
    elif B >= R and B >= G:
        hue = 4 + (R - G) / (max(rgb) - min(rgb))
    hue *= 60
    if hue < 0:
        hue += 360

    #ev3.screen.draw_text(10, 60, reflection)
    no_item = False
    if gripper_motor.angle() > -10:
        hue = -100
        no_item = True
        wait(5000)

    ev3.screen.clear()
    ev3.screen.draw_text(10, 60, hue)

    color_found = False
    if len(color_list) > 0 and not no_item:
        for color in color_list:
            diff = abs(hue - color)
            if diff > 180:
                diff = 360 - diff
            if diff <= 20:
                hue = color
                color_found = True

                break

    if not color_found and not no_item:
        color_list.append(hue)
    #ev3.screen.clear() remove #
    #ev3.screen.draw_text(10, 20, hue)
    #ev3.screen.draw_text(10, 40, len(color_list))

    return hue

def robot_pick(position):
    #pause_event.wait()
    pause_check()
    base_motor.run_target(400, position)
    #pause_event.wait()
    pause_check()
    if belt == True:
        mbox.send("Continue")
    if belt is True:
        while True:
            rgb = elbow_sensor.rgb()
            R = rgb[0]
            G = rgb[1]
            B = rgb[2]
            if R + G + B > 5:
                mbox.send("Pause") #Stop
                break
            #else:
            #    mbox.send("Continue")
    #pause_event.wait()
    pause_check()
    #elbow_motor.run_until_stalled(-60, then=Stop.HOLD, duty_limit=6)
    elbow_motor.run_target(60, 0)
    #pause_event.wait()
    pause_check()
    #if belt is True:
    #    mbox.send("Continue")
    #pause_event.wait()
    pause_check()
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    #pause_event.wait()
    pause_check()
    if belt is False:
        elbow_motor.run_target(200, 29)
    #pause_event.wait()
    pause_check()

    #gripper_motor.angle()
    #open: -90
    #closed: 5
    #gripping: -20


def robot_release(position):
    #pause_event.wait()
    pause_check()
    base_motor.run_target(400, position)
    #pause_event.wait()
    pause_check()
    elbow_motor.run_until_stalled(-100, duty_limit=-10)
    #pause_event.wait()
    pause_check()
    gripper_motor.run_target(200, -90)
    #pause_event.wait()
    pause_check()
    elbow_motor.run_target(200, 60)
    #pause_event.wait()
    pause_check()


# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

def act_based_on_color():
    detected_color = color_detection()

    if detected_color == -100:
        found_color = "no object found"
    elif detected_color <= 10:
        found_color = "red"
    elif detected_color <= 20:
        found_color = "orange"
    elif detected_color <= 70:
        found_color = "yellow"
    elif detected_color <= 165:
        found_color = "green"
    elif detected_color <= 190:
        found_color = "cyan"
    elif detected_color <= 270:
        found_color = "blue"
    elif detected_color <= 300:
        found_color = "purple"
    elif detected_color <= 340:
        found_color = "pink"
    else:
        found_color = "red"
    
    ev3.screen.draw_text(10, 20, "Current objects color:")
    ev3.screen.draw_text(10, 40, found_color)

    #pause_event.wait()
    pause_check()
    elbow_motor.run_target(200, 60)
    #pause_event.wait()
    pause_check()

    if detected_color == -100:
        #pause_event.wait()
        pause_check()
        gripper_motor.run_target(500, -90)
        #pause_event.wait()
        pause_check()

    elif detected_color == color_list[0]:
        robot_release(ZONE_1)

    elif detected_color == color_list[1]:
        robot_release(ZONE_2)

    elif detected_color == color_list[2]:
        robot_release(ZONE_3)

    elif detected_color == color_list[3]:
        robot_release(ZONE_4)


# This is the main part of the program. It is a loop that repeats endlessly.

#Threading 2/3
def main_loop():

    elbow_motor.run_target(60, 70)
    #pause_event.wait()
    pause_check()
    while True:
        #pause_event.wait()
        pause_check()
        robot_pick(ZONE_5)
        #pause_event.wait()
        pause_check()
        act_based_on_color()  # Check color and act accordingly
        #pause_event.wait()
        pause_check()

#Threading 3/3
if __name__ == "__main__":
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()

    while True:
        if Button.UP in ev3.buttons.pressed():
            if belt == True:
                mbox.send("Pause")
            pause()
        if Button.DOWN in ev3.buttons.pressed():
            if belt == True:
                mbox.send("Continue")
            resume()
        if Button.CENTER in ev3.buttons.pressed():
            if belt == True:
                mbox.send("Pause")
            shutdown()
        #elif command == "e":
        #    break
        #else:
        #    print("Invalid command")
