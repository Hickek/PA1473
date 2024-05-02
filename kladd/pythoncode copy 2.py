import threading
import time

paused = False

def pause():
    global paused
    paused = True

def resume():
    global paused
    paused = False

def is_paused():
    return paused

def another_function():
    print("Working even more...")
    time.sleep(1)
    while is_paused():
        time.sleep(0.1)

def main_loop():
    while True:
        # Do some work
        print("Working...")
        time.sleep(1)

        # Check if paused
        while is_paused():
            time.sleep(0.1)

        # More work
        print("More work...")
        time.sleep(1)

        # Check if paused
        while is_paused():
            time.sleep(0.1)

        # Even more work
        another_function()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()

    while True:
        command = input("Enter 'pause' to pause, 'resume' to resume, or 'exit' to quit: ")
        if command == "p":
            pause()
        elif command == "r":
            resume()
        elif command == "exit":
            break
        else:
            print("Invalid command")