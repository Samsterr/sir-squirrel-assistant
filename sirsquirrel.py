from src import core, mirror, mirror_utils
import argparse,logging

with open("config/status_selection.txt","r") as f:
    status = [i.strip().lower() for i in f.readlines()]

def wuthering_run(num_runs,logger):
    run_count = 0
    win_count = 0
    lose_count = 0
    status_list = (status * ((num_runs // len(status)) + 1))[:num_runs]
    logger.info("Starting Run")
    for i in range(num_runs):
        logger.info("Run {}".format(run_count + 1))
        core.md_setup()
        squad_order = mirror.set_sinner_order(status_list[i])
        run_complete = 0
        while(run_complete != 1):
            win_flag, run_complete = mirror.start_mirror(status_list[i],squad_order)

        if win_flag == 1:
            win_count += 1
        else:
            lose_count += 1
    logger.info('Won Runs {}, Lost Runs {}'.format(win_count, lose_count))

def main():
    logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (e.g., DEBUG, INFO, WARNING)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("squirrel.log"),  # Output to a file
        #logging.StreamHandler()  # Output to console
    ])
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument("RunCount",  help="How many times you want to run Mirror Dungeons")
    args = parser.parse_args()
    try:
        int(args.RunCount)
    except ValueError:
        print("Invalid Value")
        exit()

    wuthering_run(int(args.RunCount), logger)

if __name__ == "__main__":
    main()
