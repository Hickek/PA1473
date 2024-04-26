from pybricks.hubs import EV3Brick
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.tools import wait

ev3 = EV3Brick()

# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'ev3dev'

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


wait(10000)

def main():
    while True:
        if Button.LEFT in ev3.buttons.pressed():
            send_command('stop')
            wait(500)  # Debounce button press
        elif Button.RIGHT in ev3.buttons.pressed():
            send_command('start')
            wait(500)  # Debounce button press
        wait(50)

if __name__ == '__main__':
    main()

