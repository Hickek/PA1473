#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!
from pybricks.hubs import EV3Brick
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.tools import wait
#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Direction, Port, Stop, Button, Color
from pybricks.hubs import EV3Brick

ev3 = EV3Brick()

# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'ev3dev-F'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)

ev3.screen.draw_text(10, 20, 'establishing connection')
client.connect(SERVER)
ev3.screen.clear()
ev3.screen.draw_text(10, 20, 'connected')


# In this program, the client sends the first message and then waits for the
# server to reply.
mbox.send('hello World :)')
mbox.wait()
ev3.screen.clear()
#ev3.screen.draw_text(10, 20, mbox.read())

# Load belt
belt = Motor(Port.D, Direction.CLOCKWISE)
belt.control.limits(speed=150, acceleration=60)

def change_speed(change, speed):
    if -150 < speed + change <= 150:
        speed += change
        ev3.screen.print("Speed:", speed)
        belt.run(speed)
        wait(300)
    return speed

def main():
    speed = 50
    belt_on = True
    ev3.screen.print("Speed:", speed)
    belt.hold()
    wait(15000)
    belt.run(speed)

    while True:
        if Button.CENTER in ev3.buttons.pressed():
            if belt_on:
                ev3.light.on(Color.RED)
                belt.hold()
                ev3.screen.print("STOP")
            else:
                ev3.light.on(Color.GREEN)
                belt.run(speed)
                ev3.screen.print("Speed:", speed)
            belt_on = not belt_on
            wait(2000)
        if Button.UP in ev3.buttons.pressed() and belt_on:
            speed = change_speed(10, speed)
        if Button.DOWN in ev3.buttons.pressed() and belt_on:
            speed = change_speed(-10, speed)
        #wait(100)
        detected = mbox.read()

        if detected == "Stop":
            wait(300)
            belt.hold()
            wait(13000)
            belt.run(speed)
            detected = "Continue"

if __name__ == '__main__':
    main()
