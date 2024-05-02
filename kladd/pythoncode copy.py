import asyncio
import time

paused = False

async def pause():
    global paused
    paused = True

async def resume():
    global paused
    paused = False

async def is_paused():
    global paused
    return paused

async def another_function():
    print("Working even more...")
    await asyncio.sleep(1)
    while await is_paused():
        await asyncio.sleep(0.1)

async def main_loop():
    while True:
        # Do some work
        print("Working...")
        await asyncio.sleep(1)

        # Check if paused
        while await is_paused():
            await asyncio.sleep(0.1)

        # More work
        print("More work...")
        await asyncio.sleep(1)

        # Check if paused
        while await is_paused():
            await asyncio.sleep(0.1)

        # Even more work
        await another_function()

async def handle_input():
    while True:
        command = input("Enter 'pause' to pause, 'resume' to resume, or 'exit' to quit: ")
        if command == "pause":
            await pause()
        elif command == "resume":
            await resume()
        elif command == "exit":
            break
        else:
            print("Invalid command")

async def main():
    task_main_loop = asyncio.create_task(main_loop())
    task_handle_input = asyncio.create_task(handle_input())
    await asyncio.gather(task_main_loop, task_handle_input)

if __name__ == "__main__":
    asyncio.run(main())