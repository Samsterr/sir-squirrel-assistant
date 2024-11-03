import argparse
import logging
import os
import threading
import keyboard  # Import the keyboard module
from src import core, mirror,common

with open("config/status_selection.txt", "r") as f:
    status = [i.strip().lower() for i in f.readlines()]

def exit_program():
    print("\nHotkey pressed. Exiting the program...")
    os._exit(0)

# Start a background thread to listen for 'Ctrl+Q'
def start_exit_listener():
    keyboard.add_hotkey('ctrl+q', exit_program)  # Register hotkey Ctrl+Q to exit
    # Keep the listener active without blocking the main thread
    while True:
        keyboard.wait('ctrl+q')  # Block until Ctrl+Q is pressed

# Start the listener in a separate thread
exit_listener_thread = threading.Thread(target=start_exit_listener, daemon=True)
exit_listener_thread.start()

def mirror_dungeon_run(num_runs, logger):
    try:
        run_count = 0
        win_count = 0
        lose_count = 0
        status_list = (status * ((num_runs // len(status)) + 1))[:num_runs]
        logger.info("Starting Run")
        for i in range(num_runs):
            logger.info("Run {}".format(run_count + 1))
            core.md_setup()
            logger.info("Current Team: "+status_list[i])
            run_complete = 0
            MD = mirror.Mirror(status_list[i])
            while(run_complete != 1):
                win_flag, run_complete = MD.start_mirror()
            if win_flag == 1:
                win_count += 1
            else:
                lose_count += 1
            run_count += 1

        logger.info('Won Runs {}, Lost Runs {}'.format(win_count, lose_count))
    except Exception as e:
        common.error_screenshot()
        logger.error(e)

def main():
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
        handlers=[
            logging.FileHandler("squirrel.log"),  # Output to a file
        ]
    )
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument("RunCount", help="How many times you want to run Mirror Dungeons", type=int)
    args = parser.parse_args()
    mirror_dungeon_run(args.RunCount, logger)

if __name__ == "__main__":
    main()
