#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!
from pybricks.hubs import EV3Brick
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.tools import wait

ev3 = EV3Brick()

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

wait(10000)
