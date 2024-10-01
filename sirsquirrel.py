from src import core, mirror, mirror_utils

run_count = 0
num_runs = 1

with open("status_selection.txt","r") as f:
    status = [i.strip().lower() for i in f.readlines()]

status_list = (status * ((num_runs // len(status)) + 1))[:num_runs]

for i in range(num_runs):
    #core.refill_enkephalin()
    ##core.navigate_to_md()
    squad_order = mirror.set_sinner_order(status_list[i])
    run_complete = 0
    mirror.market_shopping("bleed")
    #while(run_complete != 1):
    #    mirror.start_mirror(status_list[i],squad_order, run_complete)


    
