from src import common, mirror_utils
from src.core import skill_check

def set_sinner_order(status):
    """Gets the squad order for the team status"""
    if mirror_utils.squad_choice(status) is None:
        return common.squad_order("default")
    else:
        return common.squad_order(status)
    
def floor_id():
    """Returns what floor is currently on"""
    floor = ""
    if common.element_exist('pictures/mirror/packs/floor1.png'):
        floor = "f1"
        return floor
    #if common.element_exist('pictures/mirror/packs/floor2.png'):
    #    floor = "f2"
    #    return floor
    #if common.element_exist('pictures/mirror/packs/floor3.png'):
    #    floor = "f3"
    #    return floor
    #if common.element_exist('pictures/mirror/packs/floor4.png'):
    #    floor = "f4"
    #    return floor

def check_loading():
    """Handles the loading screen transitions"""
    common.sleep(2) #Handles fade to black
    if common.element_exist("pictures/general/loading.png"): #checks for loading screen bar
        common.sleep(4) #handles the remaining loading

def transition_loading():
    """Theres a load that occurs while transitioning to the next floor"""
    common.sleep(5)

def start_mirror(status):
    """Main Mirror Logic of identifying and running the specified function"""
    if common.element_exist("pictures/mirror/general/in_progress.png"): #check if MD is in Progress
        common.click_matching("pictures/mirror/general/in_progress.png")
        common.click_matching("pictures/general/resume.png")
        check_loading() #Theres loading that occurs if you resume to Pack Selection / Navigating

    if common.element_exist("pictures/mirror/general/gift_select.png"): #Checks if in gift select
        gift_selection(status)
    
    if common.element_exist("pictures/mirror/general/squad_select.png"): #checks if in Squad select
        initial_squad_selection(status)
    
    if common.element_exist("pictures/mirror/general/reward_select.png"):
        reward_select(status)
    
    if common.element_exist("pictures/mirror/general/inpack.png"): #checks if in pack select
        refresh_flag = 0
        floor = floor_id()
        pack_selection(status,refresh_flag,floor)
    
    #if common.element_exist("pictures/mirror/explore/skip.png"):
    #    """Need to check which state it is"""
    #    state = check_state(state)
#
    #    
    #    state = "NAVIGATING" #If not its still navigating
    #    return state
    common.click_matching("pictures/mirror/general/normal.png")
    common.click_matching("pictures/general/enter.png")
    #Checks for Wish of Stars
    if common.element_exist("pictures/mirror/general/wish.png"):
        common.click_matching("pictures/general/confirm_b.png")

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
    for i in range(2):
        common.mouse_move(247,621)
        common.mouse_drag(247,1060)
    
    for i in range(4):
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

def pack_selection(status_effect,refresh_flag,floor):
    """Prioritises the status gifts for packs if not follows a list"""
    status = mirror_utils.pack_choice(status_effect)
    if status is None or (common.element_exist(status,0.75) is None and refresh_flag == 1): #Use the easy to hard list?
        with open("pictures/mirror/packs/" + floor + ".txt", "r") as f:
            packs = f.readlines()
        for i in packs:
            if common.element_exist(i):
                found = common.match_image(i)
                x,y = found[0]
                common.mouse_move(x,493)
                common.mouse_drag(x,900)
                break        
            
    if common.element_exist(status,0.75) is None and refresh_flag != 1:
        common.click_matching("pictures/mirror/general/refresh.png")
        refresh_flag = 1
        pack_selection(status,refresh_flag,floor)
    
    else:
        found = common.match_image(status,0.75)
        x,y = found[0]
        common.mouse_move(x,493)
        common.mouse_drag(x,y)
    transition_loading()

def squad_select(squad_order):
    """selects sinners in squad order"""
    common.click_matching("pictures/battle/clear.png")
    if common.element_exist("pictures/general/confirm_w.png"):
        common.click_matching("pictures/general/confirm_w.png")
    for i in squad_order:
        common.click_matching(i)
    common.key_press("enter")
    check_loading()

#needs work
def navigation(state):
    """Core navigation function to reach the end of floor"""
    node_y = [142,455,777]

    #Checks incase continuing quitted out MD
    common.click_matching("pictures/mirror/general/danteh.png")
    if common.element_exist("pictures/mirror/general/md_enter.png"):
        common.click_matching("pictures/mirror/general/md_enter.png")
        return check_state(state)
    else:
    #Find which node is the traversable one
        for i in range(3):
            common.mouse_move_click(1083,node_y[i])
            if common.element_exist("pictures/mirror/general/md_enter.png"):
                common.click_matching("pictures/mirror/general/md_enter.png")
                return check_state(state)

#needs testing
def rest_stop(status_effect):
    status = mirror_utils.enhance_gift_choice(status_effect)
    if not common.element_exist("pictures/mirror/reststop/sanity.png") or (common.element_exist("pictures/mirror/reststop/sanity.png") and len(common.match_image("pictures/mirror/reststop/sanity.png")) < 12):
        common.click_matching("pictures/mirror/reststop/heal_sinner.png")
        common.click_matching("pictures/mirror/reststop/heal_all.png")
        while(not common.element_exist("pictures/events/continue.png")):
            common.mouse_click()
        common.click_matching("pictures/events/continue.png")
        common.click_matching("pictures/general/confirm_w.png")

    common.sleep(1)
    common.click_matching("pictures/reststop/enhance.png")
    if common.element_exist(status):
        enhance_gifts = common.match_image(status)
        for i in enhance_gifts:
            x,y = i
            common.mouse_click(x,y)
            common.click_matching("pictures/mirror/reststop/power_up.png")
            if common.element_exist("pictures/mirror/reststop/confirm.png"):
                common.click_matching("pictures/mirror/reststop/confirm.png")
    common.click_matching("pictures/mirror/reststop/leave.png")

#needs testing
def reward_select(status):
    status = mirror_utils.reward_choice(status)
    if status is None or common.element_exist(status) is None:
        common.click_matching("pictures/mirror/general/reward_select.png")
    else:
        common.click_matching(status)
    common.click_matching("pictures/mirror/general/confirm_gift.png")
    common.press_matching("enter")

#needs more pics
def event_handling():
    #if common.element_exist("pictures/events/gain_check"):
    #    common.click_matching("pictures/events/gain_check")
    #    common.sleep(1)
    #    common.click_matching("pictures/events/proceed.png")
    if common.element_exist("pictures/events/gain_check"):
        common.click_matching("pictures/events/gain_check")
        common.sleep(1)
        common.click_matching("pictures/events/proceed.png")
        skill_check()

def encounter_reward_select():
    return 

def market_shopping():
    return

#untested    
def check_state(state): #dk if i need this
    """Checks which node it is currently in"""
    if common.element_exist("pictures/battle/clear.png"):
        state = "PRE_BATTLE"
        return state
    else:
        #Clearing dialog to identify
        common.click_matching("pictures/events/skip.png")
        for i in range(4):
            common.mouse_click()
        if common.element_exist("pictures/mirror/explore/event_state.png"):
            state = "EVENT"
            return state
        #if common.element_exist("pictures/mirror/explore/market_state.png"):
        #    state = "MARKET"
        #    return state
        if common.element_exist("pictures/mirror/explore/rest_state.png"):
            state = "REST_STOP"
            return state



