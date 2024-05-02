import threading
import time

class Pauser:
    def __init__(self):
        self.paused = False
        self.pause_event = threading.Event()
        self.pause_event.set()

    def pause(self):
        self.paused = True
        self.pause_event.clear()

    def resume(self):
        self.paused = False
        self.pause_event.set()

    def is_paused(self):
        return self.paused

def another_function(pauser):
    print("Working even more...")
    time.sleep(1)
    pauser.pause_event.wait()

def main_loop(pauser):
    while True:

        # Do some work
        print("Working...")
        time.sleep(1)

        # Check if paused
        pauser.pause_event.wait()

        # More work
        print("More work...")
        time.sleep(1)

        # Check if paused
        pauser.pause_event.wait()

        # Even more work
        another_function(pauser)


if __name__ == "__main__":
    pauser = Pauser()
    main_thread = threading.Thread(target=main_loop, args=(pauser,))
    main_thread.start()

    while True:
        command = input("Enter 'pause' to pause, 'resume' to resume, or 'exit' to quit: ")
        if command == "p":
            pauser.pause()
        elif command == "r":
            pauser.resume()
        elif command == "e":
            break
        else:
            print("Invalid command")
