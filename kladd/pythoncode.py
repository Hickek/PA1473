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

def main_loop(pauser):
    while True:

        print("W")
        time.sleep(1)
        pauser.pause_event.wait()
        print("Wo")
        time.sleep(1)
        pauser.pause_event.wait()
        print("Wor")
        time.sleep(1)
        pauser.pause_event.wait()
        print("Work")
        time.sleep(1)
        pauser.pause_event.wait()
        print("Worki")
        time.sleep(1)
        pauser.pause_event.wait()
        print("Workin")
        time.sleep(1)
        pauser.pause_event.wait()
        print("Working")
        time.sleep(1)
        pauser.pause_event.wait()


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
        elif command == "exit":
            break
        else:
            print("Invalid command")