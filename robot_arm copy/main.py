#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
from pybricks.tools import wait
#from pybricks.parameters import Color
from color import ClassifyColor

# Initialize the EV3 Brick
ev3 = EV3Brick()

import bluetooth

# Skapa en Bluetooth-socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Anslut till den andra EV3-enheten (ersätt XX:XX:XX:XX:XX:XX med den andra enhetens Bluetooth-adress)
sock.connect(('ev3dev', 1))

# Skicka ett kommando (som en sträng)
sock.send("python /home/robot/belt/main.py")

# Stäng anslutningen
sock.close()