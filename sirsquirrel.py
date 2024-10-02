from src import core, mirror, mirror_utils
import argparse

with open("status_selection.txt","r") as f:
    status = [i.strip().lower() for i in f.readlines()]

def wuthering_run(num_runs):
    run_count = 0
    win_count = 0
    lose_count = 0
    status_list = (status * ((num_runs // len(status)) + 1))[:num_runs]

    for i in range(num_runs):
        core.refill_enkephalin()
        core.navigate_to_md()
        squad_order = mirror.set_sinner_order(status_list[i])
        run_complete = 0

        while(run_complete != 1):
            win_flag, run_complete = mirror.start_mirror(status_list[i],squad_order)

        if win_flag == 1:
            win_count += 1
        else:
            lose_count += 1
    print('Won Runs {}, Lost Runs "{}"'.format(win_count, lose_count))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("RunCount",  help="How many times you want to run the bot")
    args = parser.parse_args()
    wuthering_run(args.RunCount)

if __name__ == "__main__":
    main()
