from pybricks.hubs import *
ev3 = EV3Brick()

filename = '/home/robot/belt/main.py'


with open(filename, 'r') as file:
    content = file.read()

# Save content to a new file on PC
with open(filename, 'w') as file:
    file.write(content)

print(f"File '{filename}' transferred successfully!")
