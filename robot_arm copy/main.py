#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
from pybricks.tools import wait
#from pybricks.parameters import Color
from color import ClassifyColor

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
elbow_motor.run_time(30, 1000)
#elbow_motor.run(-10)
#while elbow_sensor.reflection() < 28:
#    wait(10)
elbow_motor.run_until_stalled(-10, then=Stop.HOLD, duty_limit=8)
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

def robot_pick(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.

    # Rotate to the pick-up position.
    base_motor.run_target(400, position)
    # Lower the arm.
    elbow_motor.run_target(40, 0)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(200, 30)

    #gripper_motor.angle()
    #open: -90
    #closed: 5
    #gripping: -20


def robot_release(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, opens the gripper to
    # release the object. Then it raises its arm again.
    # Rotate to the drop-off position.
    base_motor.run_target(400, position)
    # Lower the arm to put the wheel stack on the ground.
    #elbow_motor.run_target(60, 0)
    elbow_motor.run_until_stalled(-100, then=Stop.COAST, duty_limit=6)
    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(200, -90)
    # Raise the arm.
    elbow_motor.run_target(200, 60)


# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

color_list = []
def color_detection():
    # Color detection v3
    # Shown at demo 1
    # Check resistance when closing claw to check if an item is present
    # Also use resistance to place on elevated positions (when items are stacked)

    rgb = elbow_sensor.rgb()
    return ClassifyColor(rgb)
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

    color_found = False
    if len(color_list) > 0 and not no_item:
        for color in color_list:
            diff = abs(hue - color)
            if diff > 180:
                diff = 360 - diff
            if diff <= 30:
                hue = color
                color_found = True
                break

    if not color_found and not no_item:
        color_list.append(hue)
    ev3.screen.clear()
    ev3.screen.draw_text(10, 20, hue)
    ev3.screen.draw_text(10, 40, len(color_list))

    return hue

def color_detection_2():
    # Color detection v4
    # Not yet tested
    # Takes brightness of the color into account
    # Not sure that is a good thing thought as the small pieces are seen as darker than the large pieces

    rgb = elbow_sensor.rgb()
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    reflection = (r + g + b) / 3
    no_item = False
    if reflection <= 12:
        hue = -100
        no_item = True

    color_found = False
    if max(rgb) == min(rgb):
        difference = -1
    else:
        if len(color_list) > 0 and not no_item:
            for color in color_list:
                r_diff = abs(r - color[0])
                g_diff = abs(g - color[1])
                b_diff = abs(b - color[2])
                difference = (r_diff ** 2 + g_diff ** 2 + b_diff ** 2) ** 0.5
                if difference <= 10:
                    hue = color
                    color_found = True
                    break

    if not color_found and not no_item:
        color_list.append(hue)

    return hue

def act_based_on_color():
    detected_color = color_detection()
    if detected_color == -100:
        ev3.screen.draw_text(10, 80, "No item found")
        gripper_motor.run_target(500, -90)

    elif detected_color == "yellow":
        robot_release(RIGHT)

    elif detected_color == "red":
        robot_release(MID)
       
    elif detected_color == "blue":
        robot_release(LEFT)

    elif detected_color == "green":
        robot_release(EXTRA)

# Define the four destinations for picking up and moving the wheel stacks.
PICKUP = 5
EXTRA = 45
RIGHT = 102
MID = 155
LEFT = 205

# This is the main part of the program. It is a loop that repeats endlessly.
#
# First, the robot moves the object on the left towards the middle.
# Second, the robot moves the object on the right towards the left.
# Finally, the robot moves the object that is now in the middle, to the right.
#
# Now we have a wheel stack on the left and on the right as before, but they
# have switched places. Then the loop repeats to do this over and over.

elbow_motor.run_target(60, 70)
while True:
    # M
    robot_pick(PICKUP)
    act_based_on_color()  # Check color and act accordingly
