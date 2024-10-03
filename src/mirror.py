from src import common, mirror_utils
from src.core import skill_check, battle

def set_sinner_order(status):
    """Gets the squad order for the team status"""
    if mirror_utils.squad_choice(status) is None:
        return common.squad_order("default")
    else:
        return common.squad_order(status)
    
def floor_id():
    """Returns what floor is currently on"""
    floor = ""
    if common.element_exist('pictures/mirror/packs/floor1.png',0.9):
        floor = "f1"
    if common.element_exist('pictures/mirror/packs/floor2.png',0.9):
        floor = "f2"
    if common.element_exist('pictures/mirror/packs/floor3.png',0.9):
        floor = "f3"
    if common.element_exist('pictures/mirror/packs/floor4.png',0.9):
        floor = "f4"
    return floor

def check_loading():
    """Handles the loading screen transitions"""
    common.sleep(2) #Handles fade to black
    if common.element_exist("pictures/general/loading.png"): #checks for loading screen bar
        print("LOADING")
        common.sleep(5) #handles the remaining loading

def transition_loading():
    """Theres a load that occurs while transitioning to the next floor"""
    common.sleep(5)

def start_mirror(status, squad_order):
    run_complete = 0
    win_flag = 0
    """Main Mirror Logic of identifying and running the specified function"""
    if common.element_exist("pictures/mirror/general/in_progress.png"): #check if MD is in Progress
        common.click_matching("pictures/mirror/general/in_progress.png")
        common.click_matching("pictures/general/resume.png")
        print("CONTINUING RUN")
        check_loading() #Theres loading that occurs if you resume to Pack Selection / Navigating

    if common.element_exist("pictures/mirror/general/in_progress.png") is None and common.element_exist("pictures/mirror/general/normal.png"):
        #Checks for MD not started
        common.click_matching("pictures/mirror/general/normal.png")
        common.click_matching("pictures/general/enter.png")
        #Checks for Wish of Stars
        if common.element_exist("pictures/mirror/general/wish.png"):
            common.click_matching("pictures/general/confirm_b.png")
            print("STARTING RUN")
    
    if common.element_exist("pictures/general/maint.png"):
        common.click_matching("pictures/general/confirm_b.png")
        common.click_matching("pictures/general/no_op.png")
        common.click_matching("pictures/general/confirm_b.png")
        print("SERVER UNDERGOING MAINTAINANCE, BOT WILL STOP")
        exit()

    #if common.element_exist("pictures/general/explore_reward.png"):
        #check bp
        #if not give up

    if common.element_exist("pictures/general/defeat.png"):
        print("RUN LOST")
        defeat()
        run_complete = 1
        win_flag = 0
        return run_complete,win_flag
    
    if common.element_exist("pictures/general/victory.png"):
        print("RUN WIN")
        victory()
        run_complete = 1
        win_flag = 1
        return run_complete,win_flag
    
    if common.element_exist("pictures/mirror/general/gift_select.png"): #Checks if in gift select
        print("GIFT SELECT")
        gift_selection(status)
    
    if common.element_exist("pictures/mirror/general/squad_select.png"): #checks if in Squad select
        print("INITIAL SQUAD SELECT")
        initial_squad_selection(status)

    if common.element_exist("pictures/mirror/general/inpack.png"): #checks if in pack select
        print("SELECTING PACK")
        refresh_flag = 0
        pack_selection(status,refresh_flag)
    
    if common.element_exist("pictures/mirror/general/danteh.png"): #checks if currently navigating
        print("NAVIGATING")
        navigation()

    if common.element_exist("pictures/battle/clear.png"): #checks if in squad select and then proceeds with battle
        print("SELECTING SQUAD")
        squad_select(squad_order)
    
    if common.element_exist("pictures/battle/winrate.png"):
        print("STARTING BATTLE")
        battle()
    
    if common.element_exist("pictures/mirror/general/event.png"):
        print("EVENT")
        event_choice()

    if common.element_exist("pictures/mirror/reststop/fuse.png"): #checks if in rest stop
        print("REST STOP")
        rest_stop(status)

    if common.element_exist("pictures/mirror/market/sell_gifts.png"): #checks if in market
        print("MARKET")
        market_shopping(status)

    if common.element_exist("pictures/mirror/general/reward_select.png"): #checks if in reward select
        print("REWARD SELECT")
        reward_select(status)
    
    if common.element_exist("pictures/mirror/general/encounter_reward.png"): #checks if in encounter rewards
        print("ENCOUNTER REWARD SELECT")
        encounter_reward_select()

    if common.element_exist("pictures/events/skip.png"): #if hitting the events click skip to determine which is it
        print("? NODE")
        common.click_matching("pictures/events/skip.png")
        for _ in range(4):
            common.mouse_click()

    return win_flag,run_complete

def gift_selection(status):
    """selects the ego gift of the same status, fallsback on random if not unlocked"""
    initial_gift_coords = [420,580,740]
    if status == "sinking":
           initial_gift_coords.pop(0)
    else:
           initial_gift_coords.pop(2)

    gift = mirror_utils.gift_choice(status)
    if gift is None:
        gift = "pictures/mirror/gifts/random.png"

    if common.element_exist(gift,0.9) is None: #Search for gift and if not present scroll to find it
        common.mouse_move(320,289)
        common.mouse_drag(320,89)

    common.click_matching(gift,0.9) #click on specified
    common.mouse_move_click(1230,initial_gift_coords[0])
    common.mouse_move_click(1230,initial_gift_coords[1])
    common.click_matching("pictures/mirror/general/confirm_gift.png")
    common.key_press("esc")
    common.sleep(1)
    common.key_press("esc")

def initial_squad_selection(squad_status):
    """Searches for the squad name with the status type, if not found then uses the current squad"""
    status = mirror_utils.squad_choice(squad_status)
    if status is None:
        common.click_matching("pictures/general/squad_confirm.png")
        return
    
    #This is to bring us to the first entry of teams
    for _ in range(2):
        common.mouse_move(247,621)
        common.mouse_drag(247,1060)
    
    #scrolls through all the squads in steps to look for the name
    for _ in range(4):
        if common.element_exist(status,0.9) is None:
            common.mouse_move(247,621)
            common.mouse_drag(247,435)
            common.sleep(5)
            continue
        else:
            common.click_matching(status,0.9)
            break

    common.click_matching("pictures/general/squad_confirm.png")
    check_loading() #Theres a load screen when going from Squad to Pack


def pack_selection(status_effect,refresh_flag):
    """Prioritises the status gifts for packs if not follows a list"""
    status = mirror_utils.pack_choice(status_effect)
    floor = floor_id()

    if refresh_flag == 0:
        #Skip certain packs appearing that interfere with logic like Bamboo Kim + Skin Prophet
        if status is None or common.element_exist("pictures/mirror/packs/f4/burning.png")\
            or common.element_exist("pictures/mirror/packs/f3/slicers.png")\
            or common.element_exist("pictures/mirror/packs/f4/wrath.png")\
            or common.element_exist("pictures/mirror/packs/f4/yield.png")\
            or common.element_exist("pictures/mirror/packs/f2/violet.png"):

            common.click_matching("pictures/mirror/general/refresh.png")
            refresh_flag = 1
            pack_selection(status,refresh_flag)
        else:
            found = common.match_image(status,0.75)
            x,y = common.random_choice(found) #seems to prioritse the last item detected so i added this to add some differences
            common.mouse_move(x,493)
            common.mouse_drag(x,y)
            transition_loading() #Floor transitions after pack selection
        
    elif refresh_flag == 1:
        #Skip certain packs appearing that interfere with logic like Bamboo Kim + Skin Prophet
        if status is None or common.element_exist("pictures/mirror/packs/f4/burning.png")\
            or common.element_exist("pictures/mirror/packs/f3/slicers.png")\
            or common.element_exist("pictures/mirror/packs/f4/wrath.png")\
            or common.element_exist("pictures/mirror/packs/f4/yield.png")\
            or common.element_exist("pictures/mirror/packs/f2/violet.png"):

            with open("config/" + floor + ".txt", "r") as f:
                packs = [i.strip() for i in f.readlines()] #uses the f1,f2,f3,f4 txts for floor order
            for i in packs:
                if common.element_exist(i):
                    found = common.match_image(i)
                    x,y = common.random_choice(found)
                    common.mouse_move(x,493)
                    common.mouse_drag(x,900)
                    break
            transition_loading()

        else:
            #use the ego gift status
            found = common.match_image(status,0.75)
            x,y = common.random_choice(found)
            common.mouse_move(x,493)
            common.mouse_drag(x,y)
            transition_loading()
        
def squad_select(squad_order):
    """selects sinners in squad order"""
    common.click_matching("pictures/battle/clear.png")
    if common.element_exist("pictures/general/confirm_w.png"):
        common.click_matching("pictures/general/confirm_w.png")
    for i in squad_order: #click squad members according to the order in the json file
        x,y = i
        common.mouse_move_click(x,y)
    common.key_press("enter")
    check_loading()

def reward_select(status):
    """Selecting EGO Gift rewards"""
    status = mirror_utils.reward_choice(status)
    if status is None or common.element_exist(status) is None:
        common.click_matching("pictures/mirror/general/reward_select.png")
    else:
        common.click_matching(status)
    common.click_matching("pictures/mirror/general/confirm_gift.png")
    common.key_press("enter")

def encounter_reward_select():
    """Select Encounter Rewards prioritising starlight first"""
    encounter_reward = ["pictures/mirror/encounter_reward/starlight.png",
                        "pictures/mirror/encounter_reward/cost_gift.png",
                        "pictures/mirror/encounter_reward/gift.png",
                        "pictures/mirror/encounter_reward/cost.png",
                        "pictures/mirror/encounter_reward/resource.png.png"]
    
    for rewards in encounter_reward:
        if common.element_exist(rewards):
            common.click_matching(rewards)
            common.click_matching("pictures/general/confirm_b.png")
            #ommon.sleep(1)
            if common.element_exist("pictures/mirror/general/ego_gift_get.png"): #handles the ego gift get
                common.click_matching("pictures/general/confirm_b.png")
            break
    common.sleep(3) #needs to wait for the gain to credits

#needs work
def navigation():
    """Core navigation function to reach the end of floor"""
    node_y = [455,142,777] #Middle node is the most occuring so its first

    #Checks incase continuing quitted out MD
    common.click_matching("pictures/mirror/general/danteh.png")
    if common.element_exist("pictures/mirror/general/md_enter.png"):
        common.click_matching("pictures/mirror/general/md_enter.png")
    else:
    #Find which node is the traversable one
        for i in range(3):
            common.mouse_move_click(1083,node_y[i])
            if common.element_exist("pictures/mirror/general/md_enter.png"):
                common.click_matching("pictures/mirror/general/md_enter.png")

def market_shopping(status_effect):
    """Handles Market Node"""
    #If everyone not at 45 sanity then heal
    refresh_flag = 0
    status = mirror_utils.market_choice(status_effect)

    #Check for insufficient cost to exit
    if common.element_exist("pictures/mirror/market/small_not.png"):
        common.click_matching("pictures/mirror/market/leave.png")
        common.click_matching("pictures/general/confirm_w.png")
    
    else:
        if not common.element_exist("pictures/mirror/reststop/sanity.png") or (common.element_exist("pictures/mirror/reststop/sanity.png")\
        and len(common.match_image("pictures/mirror/reststop/sanity.png")) < 12):
            #Click on heal and heal all, then click til the continue prompt shows up
            common.click_matching("pictures/mirror/market/heal.png")
            if common.element_exist("pictures/mirror/market/heal_all.png"): #if you cant afford this will not show up so check for it
                common.click_matching("pictures/mirror/market/heal_all.png")
                while(not common.element_exist("pictures/events/continue.png")):
                    common.mouse_click()
                common.click_matching("pictures/events/continue.png")

        if status is not None:
            while(refresh_flag != 2):
                if common.element_exist(status):
                    enhance_gifts = common.match_image(status)
                    for i in enhance_gifts:
                        x,y = i
                        common.mouse_move_click(x,y)
                        if common.element_exist("pictures/mirror/market/purchase.png"): #purchase button will appear if purchasable
                            common.click_matching("pictures/mirror/market/purchase.png")
                            common.click_matching("pictures/general/confirm_b.png")
                    common.click_matching("pictures/mirror/market/refresh.png")
                    refresh_flag += 1

                else:
                    common.click_matching("pictures/mirror/market/refresh.png")
                    refresh_flag += 1

        common.click_matching("pictures/mirror/market/leave.png")
        common.click_matching("pictures/general/confirm_w.png")

def rest_stop(status_effect):
    #check for insufficient cost
    if common.element_exist("pictures/mirror/reststop/no_cost.png"):
        common.click_matching("pictures/mirror/reststop/leave.png")
        common.click_matching("pictures/general/confirm_w.png")

    else:
        status = mirror_utils.enhance_gift_choice(status_effect)
        if not common.element_exist("pictures/mirror/reststop/sanity.png") or (common.element_exist("pictures/mirror/reststop/sanity.png")\
        and len(common.match_image("pictures/mirror/reststop/sanity.png")) < 12):

            common.click_matching("pictures/mirror/reststop/heal_sinner.png")
            if common.element_exist("pictures/mirror/reststop/heal_all.png"): #checks if prompt does enter
                common.click_matching("pictures/mirror/reststop/heal_all.png") #This is to check for successful healing
                common.click_matching("pictures/events/skip.png")
                for i in range(3):
                    common.mouse_click() #clearing the dialog to check for continue
                if common.element_exist("pictures/events/continue.png"): #successful heal
                    common.click_matching("pictures/events/continue.png")
                else:
                    common.click_matching("pictures/mirror/reststop/back.png")#unsuccessful heal 

        common.sleep(1)
        common.click_matching("pictures/mirror/reststop/enhance.png")
        if common.element_exist("pictures/mirror/reststop/scroll_bar.png"): #if scroll bar present scrolls to the start
            common.click_matching("pictures/mirror/reststop/scroll_bar.png")
            for i in range(5):
                common.mouse_scroll(1000)
        
        enhance_gifts(status)

        common.click_matching("pictures/mirror/reststop/close.png")
        common.click_matching("pictures/mirror/reststop/leave.png")
        common.click_matching("pictures/general/confirm_w.png")

def enhance_gifts(status):
    """Enhancement gift process"""
    for _ in range(2):
        if common.element_exist(status):
            gifts = common.match_image(status)
            for i in gifts:
                x,y = i
                for _ in range(2): #upgrading twice
                    common.mouse_move_click(x,y)
                    if common.element_exist("pictures/mirror/reststop/fully_upgraded.png"): #if fully upgraded skip this item
                        break
                    common.click_matching("pictures/mirror/reststop/power_up.png")
                    if common.element_exist("pictures/mirror/reststop/more.png"): #If player has no more cost exit
                        common.click_matching("pictures/mirror/reststop/cancel.png")
                        common.click_matching("pictures/mirror/reststop/close.png")
                        return
                    elif common.element_exist("pictures/mirror/reststop/confirm.png"):
                        common.click_matching("pictures/mirror/reststop/confirm.png")

        if common.element_exist("pictures/mirror/reststop/scroll_bar.png"):
            common.click_matching("pictures/mirror/reststop/scroll_bar.png")
            for k in range(5):
                common.mouse_scroll(-1000)

def event_choice():
    if common.element_exist("pictures/events/select_gain.png"): #Select to gain EGO Gift
        common.click_matching("pictures/events/select_gain.png")
        while(not common.element_exist("pictures/events/continue.png")):
            common.mouse_click()
        common.click_matching("pictures/events/continue.png")
        #if common.element_exist("pictures/mirror/general/ego_gift_get.png"): #handles the ego gift get
        #common.click_matching("pictures/general/confirm_b.png")
        common.key_press("enter")

    if common.element_exist("pictures/events/gain_check.png"): #Pass to gain an EGO Gift
        common.click_matching("pictures/events/gain_check.png")
        common.click_matching("pictures/events/proceed.png")
        skill_check()

    if common.element_exist("pictures/events/gain_gift.png"): #Proceed to gain
        common.click_matching("pictures/events/gain_gift.png")
        while(not common.element_exist("pictures/events/proceed.png")):
            common.mouse_click()
        common.click_matching("pictures/events/proceed.png")
        if common.element_exist("pictures/events/skip.png"):
            common.click_matching("pictures/events/skip.png")
            for _ in range(4):
                common.mouse_click()
            event_choice()
    
    if common.element_exist("pictures/events/win_battle.png"): #Win battle to gain
        common.click_matching("pictures/events/win_battle.png")
        while(not common.element_exist("pictures/events/commence_battle.png")):
            common.mouse_click()
        common.click_matching("pictures/events/commence_battle.png")

def victory():
    common.click_matching("pictures/general/beeg_confirm.png")
    common.click_matching("pictures/general/claim_rewards.png")
    common.click_matching("pictures/general/md_claim.png")
    if common.element_exist("pictures/general/confirm_w.png"):
        print("Rewards Claimed")
        common.click_matching("pictures/general/confirm_w.png")
        common.click_matching("pictures/general/confirm_b.png")
        check_loading()
    else: #incase not enough modules
        common.click_matching("pictures/general/to_window.png")
        common.click_matching("pictures/general/confirm_w.png")
        check_loading()
        print("You dont have enough modules to continue")
        exit() 

def defeat():
    common.click_matching("pictures/general/beeg_confirm.png")
    common.click_matching("pictures/general/give_up.png")
    common.click_matching("pictures/general/confirm_w.png")
    check_loading()