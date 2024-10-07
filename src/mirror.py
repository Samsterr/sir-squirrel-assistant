from src import common, mirror_utils
from src.core import skill_check, battle
import logging

logger = logging.getLogger(__name__)

def set_sinner_order(status):
    """Gets the squad order for the team status"""
    if mirror_utils.squad_choice(status) is None:
        return common.squad_order("default")
    else:
        return common.squad_order(status)
    
def floor_id():
    """Returns what floor is currently on"""
    floor = ""
    if common.element_exist('pictures/mirror/packs/floor1.png',0.95):
        floor = "f1"
    if common.element_exist('pictures/mirror/packs/floor2.png',0.95):
        floor = "f2"
    if common.element_exist('pictures/mirror/packs/floor3.png',0.95):
        floor = "f3"
    if common.element_exist('pictures/mirror/packs/floor4.png',0.95):
        floor = "f4"
    return floor

def check_loading():
    """Handles the loading screen transitions"""
    common.sleep(2) #Handles fade to black
    if common.element_exist("pictures/general/loading.png"): #checks for loading screen bar
        logger.info("Loading")
        common.sleep(5) #handles the remaining loading

def transition_loading():
    """Theres a load that occurs while transitioning to the next floor"""
    logger.info("Moving to Next Floor")
    common.sleep(5)

def start_mirror(status, squad_order):
    run_complete = 0
    win_flag = 0
    """Main Mirror Logic of identifying and running the specified function"""
    if common.element_exist("pictures/mirror/general/in_progress.png"): #check if MD is in Progress
        common.click_matching("pictures/mirror/general/in_progress.png")
        common.click_matching("pictures/general/resume.png")
        logger.info("Resuming Run")
        check_loading() #Theres loading that occurs if you resume to Pack Selection / Navigating

    if common.element_exist("pictures/mirror/general/in_progress.png") is None and common.element_exist("pictures/mirror/general/normal.png"):
        #Checks for MD not started
        common.click_matching("pictures/mirror/general/normal.png")
        common.click_matching("pictures/general/enter.png")
        #Checks for Wish of Stars
        if common.element_exist("pictures/mirror/general/wish.png"):
            common.click_matching("pictures/general/confirm_b.png")
            logger.info("Starting Run")
    
    if common.element_exist("pictures/general/maint.png"):
        common.click_matching("pictures/general/confirm_b.png")
        common.click_matching("pictures/general/no_op.png")
        common.click_matching("pictures/general/confirm_b.png")
        logger.info("SERVER UNDERGOING MAINTAINANCE, BOT WILL STOP NOW!")
        exit()

    #if common.element_exist("pictures/general/explore_reward.png"):
        #check bp
        #if not give up

    if common.element_exist("pictures/general/defeat.png"):
        defeat()
        run_complete = 1
        win_flag = 0
        return win_flag,run_complete
    
    if common.element_exist("pictures/general/victory.png"):
        victory()
        run_complete = 1
        win_flag = 1
        return win_flag,run_complete
    
    if common.element_exist("pictures/mirror/general/gift_select.png"): #Checks if in gift select
        gift_selection(status)
    
    if common.element_exist("pictures/mirror/general/squad_select.png"): #checks if in Squad select
        initial_squad_selection(status)

    if common.element_exist("pictures/mirror/general/inpack.png"): #checks if in pack select
        pack_selection(status)
    
    if common.element_exist("pictures/mirror/general/danteh.png"): #checks if currently navigating
        navigation()

    if common.element_exist("pictures/battle/clear.png"): #checks if in squad select and then proceeds with battle
        squad_select(squad_order)
    
    if common.element_exist("pictures/battle/winrate.png"):
        battle()
    
    if common.element_exist("pictures/mirror/general/event.png"):
        event_choice()

    if common.element_exist("pictures/mirror/reststop/fuse.png"): #checks if in rest stop
        rest_stop(status)

    if common.element_exist("pictures/mirror/market/sell_gifts.png"): #checks if in market
        market_shopping(status)

    if common.element_exist("pictures/mirror/general/reward_select.png"): #checks if in reward select
        reward_select(status)
    
    if common.element_exist("pictures/mirror/general/encounter_reward.png"): #checks if in encounter rewards
        encounter_reward_select()

    if common.element_exist("pictures/events/skip.png"): #if hitting the events click skip to determine which is it
        logger.info("Entered ? node")
        common.click_skip(4)

    return win_flag,run_complete

def gift_selection(status):
    """selects the ego gift of the same status, fallsback on random if not unlocked"""
    logger.info("E.G.O Gift Selection")
    initial_gift_coords = [420,580,740] #The side bar location for EGO Gifts
    if status == "sinking": #Other 2 gifts better
           initial_gift_coords.pop(0)
    else:
           initial_gift_coords.pop(2)

    gift = mirror_utils.gift_choice(status)
    if gift is None: 
        gift = "pictures/mirror/gifts/random.png" #Use Random in the event statuses have not been unlocked

    if common.element_exist(gift,0.9) is None: #Search for gift and if not present scroll to find it
        common.mouse_move(320,289)
        for i in range(5):
            common.mouse_scroll(-1000)

    common.click_matching(gift,0.9) #click on specified
    common.mouse_move_click(1230,initial_gift_coords[0])
    common.mouse_move_click(1230,initial_gift_coords[1])
    common.click_matching("pictures/mirror/general/confirm_gift.png")
    common.key_press("esc")
    common.sleep(1)
    common.key_press("esc")

def initial_squad_selection(squad_status):
    """Searches for the squad name with the status type, if not found then uses the current squad"""
    logger.info("Mirror Dungeon Squad Select")
    status = mirror_utils.squad_choice(squad_status)
    if status is None:
        common.click_matching("pictures/general/squad_confirm.png")
        return
    
    #This is to bring us to the first entry of teams
    common.mouse_move(247,621)
    for i in range(30):
        common.mouse_scroll(1000)
    #scrolls through all the squads in steps to look for the name
    for _ in range(4):
        if common.element_exist(status) is None:
            common.mouse_move(247,621)
            for i in range(7):
                common.mouse_scroll(-1000)
            common.sleep(1)
            continue
        else:
            common.click_matching(status)
            break

    common.click_matching("pictures/general/squad_confirm.png")
    check_loading() #Theres a load screen when going from Squad to Pack


def pack_selection(status_effect):
    """Prioritises the status gifts for packs if not follows a list"""
    logger.info("Selecting Pack")
    status = mirror_utils.pack_choice(status_effect)
    if status is None:
        status = "pictures/mirror/packs/status/poise_pack.png" #Default to poise
    floor = floor_id()
    logger.debug("Current Floor "+ floor)
    found = common.match_image("pictures/mirror/general/refresh.png")
    x,y = found[0]
    logger.debug(common.luminence(x-3,y))
    refresh_flag = common.luminence(x-3,y) < 13

    if exclusion_detection(floor) and not refresh_flag: #if pack exclusion detected and not refreshed
        logger.debug("PACKS: pack exclusion detected, refreshing")
        common.click_matching("pictures/mirror/general/refresh.png")
        common.mouse_move(200,200)
        pack_selection(status_effect)

    if exclusion_detection(floor) and refresh_flag: #if pack exclusion detected and refreshed
        logger.debug("PACKS: pack exclusion detected and refreshed, choosing from pack")
        return pack_list(floor)
        
    if common.element_exist(status, 0.75) and not exclusion_detection(floor): #if pack exclusion absent and status exists
        logger.debug("pack exclusion not detected, choosing from status")
        return choose_pack(status)
    
    if common.element_exist(status,0.75) and exclusion_detection(floor) and not refresh_flag: #if pack detected and status detected and not refreshed
        logger.debug("PACKS: pack exclusion detected, status detected, refreshing")
        common.click_matching("pictures/mirror/general/refresh.png")
        pack_selection(status_effect)

    else:
        logger.debug("PACKS: using pack list")
        return pack_list(floor)

def pack_list(floor):
    with open("config/" + floor + ".txt", "r") as f:
        packs = [i.strip() for i in f.readlines()] #uses the f1,f2,f3,f4 txts for floor order
    for i in packs:
        if common.element_exist(i,0.75):
            return choose_pack(i)

def choose_pack(pack_image):
    found = common.match_image(pack_image, 0.75)
    x,y = found[0]
    common.mouse_move(x,493)
    common.mouse_drag(x,900)
    transition_loading()
    return

def exclusion_detection(floor):
    """Detects an excluded pack"""
    detected = 0
    if floor == "f1":
        return detected
    if floor == "f2":
        exclusion = ["pictures/mirror/packs/f2/violet.png"]

    if floor == "f3":    
        exclusion = ["pictures/mirror/packs/f3/crawling.png",
                   "pictures/mirror/packs/f3/slicers.png",
                   "pictures/mirror/packs/f3/flood.png"]
    if floor == "f4":
        exclusion = ["pictures/mirror/packs/f4/wrath.png",
                   "pictures/mirror/packs/f4/burning.png",
                   "pictures/mirror/packs/f4/yield.png",
                   "pictures/mirror/packs/f4/sloth.png"]
    for i in exclusion:
        if common.element_exist(i, 0.75):
            detected = 1
            return detected
    return detected
    
def squad_select(squad_order):
    """selects sinners in squad order"""
    logger.info("Selecting Squad for Battle")
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
    logger.info("Reward Selection")
    status_effect = mirror_utils.reward_choice(status)
    if status_effect is None:
        status_effect = "pictures/mirror/rewards/poise_reward.png"
    if common.element_exist(status_effect) is None:
        common.click_matching("pictures/mirror/general/reward_select.png")
    else:
        common.click_matching(status_effect)
    
    common.click_matching("pictures/mirror/general/confirm_gift.png")
    common.key_press("enter")

def encounter_reward_select():
    """Select Encounter Rewards prioritising starlight first"""
    logger.info("Encounter Reward Selection")
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
    logger.info("Navigating")
    node_y = [455,142,777,605] #Middle node is the most occuring so its first

    #Checks incase continuing quitted out MD
    common.click_matching("pictures/mirror/general/danteh.png")
    if common.element_exist("pictures/mirror/general/md_enter.png"):
        common.click_matching("pictures/mirror/general/md_enter.png")
    else:
    #Find which node is the traversable one
        for i in range(3):
            common.mouse_move_click(1083,node_y[i])
            common.sleep(1)
            if common.element_exist("pictures/mirror/general/md_enter.png"):
                common.key_press("enter")
                break

def market_shopping(status_effect):
    """Handles Market Node"""
    #If everyone not at 45 sanity then heal
    logger.info("Marketplace")
    refresh_flag = 0
    status = mirror_utils.market_choice(status_effect)
    if status is None:
        status = "pictures/mirror/market/poise_market.png"

    #Check for insufficient cost to exit
    if common.element_exist("pictures/mirror/market/small_not.png"):
        logger.debug("MARKET: Not enough cost, exiting market")
        common.click_matching("pictures/mirror/market/leave.png")
        common.click_matching("pictures/general/confirm_w.png")
    
    else:
        #if not common.element_exist("pictures/mirror/reststop/sanity.png") or (common.element_exist("pictures/mirror/reststop/sanity.png")\
        #and len(common.match_image("pictures/mirror/reststop/sanity.png")) < 12):
        #    #Click on heal and heal all, then click til the continue prompt shows up
        common.click_matching("pictures/mirror/market/heal.png")
        if common.element_exist("pictures/mirror/market/heal_all.png"): #if you cant afford this will not show up so check for it
            logger.debug("MARKET: HEALING ALL")
            common.click_matching("pictures/mirror/market/heal_all.png")
            common.wait_skip("pictures/events/continue.png")

        for _ in range(3):
            if common.element_exist(status):
                market_gifts = common.match_image(status)
                for i in market_gifts:
                    x,y = i
                    logger.debug(common.luminence(x+31,y+1))
                    if common.luminence(x+31,y+1) < 6: #this area will have a value of less than or equal to 5 if purchased
                        continue
                    if common.element_exist("pictures/mirror/market/small_not.png"):
                        logger.debug("MARKET: NOT ENOUGH COST AFTER PURCHASE, EXITING MARKET")
                        break
                    common.mouse_move_click(x,y)
                    if common.element_exist("pictures/mirror/market/purchase.png"): #purchase button will appear if purchasable
                        logger.debug("MARKET: PURCHASED EGO GIFT")
                        common.click_matching("pictures/mirror/market/purchase.png")
                        common.click_matching("pictures/general/confirm_b.png")
                if common.element_exist("pictures/mirror/market/small_not.png"):
                    break
                
            if _ != 2:
                common.click_matching("pictures/mirror/market/refresh.png")

        common.click_matching("pictures/mirror/market/leave.png")
        common.click_matching("pictures/general/confirm_w.png")

def rest_stop(status_effect):
    #check for insufficient cost
    logger.info("Rest Stop")
    if common.element_exist("pictures/mirror/reststop/no_cost.png"):
        logger.debug("REST STOP: NOT ENOUGH COST, EXITING REST STOP")
        common.click_matching("pictures/mirror/reststop/no_cost.png")
        common.click_matching("pictures/mirror/reststop/leave.png")
        common.click_matching("pictures/general/confirm_w.png")

    else:
        status = mirror_utils.enhance_gift_choice(status_effect)
        if status is None:
            status = "pictures/mirror/reststop/poise_enhance.png"
        #if not common.element_exist("pictures/mirror/reststop/sanity.png") or (common.element_exist("pictures/mirror/reststop/sanity.png")\
        #and len(common.match_image("pictures/mirror/reststop/sanity.png")) < 12): #Heal if all 12 sinners arent 45 Sanity

        common.click_matching("pictures/mirror/reststop/heal_sinner.png")
        if common.element_exist("pictures/mirror/reststop/heal_all.png"): #checks if prompt does enter
            common.click_matching("pictures/mirror/reststop/heal_all.png") #This is to check for successful healing
            common.click_matching("pictures/events/skip.png")
            for i in range(3):
                common.mouse_click() #clearing the dialog to check for continue
            if common.element_exist("pictures/events/continue.png"): #successful heal
                logger.debug("REST STOP: HEALING ALL SINNERS")
                common.click_matching("pictures/events/continue.png")
            else:
                logger.debug("REST STOP: UNSUCCESSFULLY HEALED SINNERS")
                common.click_matching("pictures/mirror/reststop/back.png")#unsuccessful heal 

        common.click_matching("pictures/mirror/reststop/enhance.png")
        logger.debug("REST STOP: ENHANCING EGO GIFTS")
        if common.element_exist("pictures/mirror/reststop/scroll_bar.png"): #if scroll bar present scrolls to the start
            common.click_matching("pictures/mirror/reststop/scroll_bar.png")
            for i in range(5):
                common.mouse_scroll(1000)
        shift_x, shift_y = mirror_utils.enhance_shift(status_effect)
        if shift_x is None or shift_y is None:
            shift_x = 9
            shift_y = -30
        enhance_gifts(status, shift_x, shift_y)
        if common.element_exist("pictures/mirror/reststop/close.png"):
            common.click_matching("pictures/mirror/reststop/close.png")
        common.click_matching("pictures/mirror/reststop/leave.png")
        common.click_matching("pictures/general/confirm_w.png")

def enhance_gifts(status, shift_x, shift_y):
    """Enhancement gift process"""
    for _ in range(2):
        if common.element_exist(status):
            gifts = common.match_image(status)
            for i in gifts:
                x,y = i
                logger.debug(common.luminence(x+shift_x,y+shift_y))
                if common.luminence(x+shift_x,y+shift_y) < 21: #19.66 is for upgraded and 14.33 is for greyed out so 20 should work for now
                    continue
                for _ in range(2): #upgrading twice
                    common.mouse_move_click(x,y)
                    if common.element_exist("pictures/mirror/reststop/fully_upgraded.png"): #if fully upgraded skip this item
                        break
                    common.click_matching("pictures/mirror/reststop/power_up.png")
                    if common.element_exist("pictures/mirror/reststop/more.png"): #If player has no more cost exit
                        logger.debug("REST STOP: NOT ENOUGH COST, EXITING ENHANCE PAGE")
                        common.click_matching("pictures/mirror/reststop/cancel.png")
                        common.sleep(1)
                        common.mouse_click()
                        return
                    elif common.element_exist("pictures/mirror/reststop/confirm.png"):
                        logger.debug("REST STOP: EGO GIFT UPGRADED")
                        common.click_matching("pictures/mirror/reststop/confirm.png")

        if common.element_exist("pictures/mirror/reststop/scroll_bar.png"):
            common.click_matching("pictures/mirror/reststop/scroll_bar.png")
            for k in range(5):
                common.mouse_scroll(-1000)

def event_choice():
    logger.info("Event")
    if common.element_exist("pictures/events/select_gain.png"): #Select to gain EGO Gift
        logger.debug("Select to gain EGO Gift")
        common.click_matching("pictures/events/select_gain.png")
        common.wait_skip("pictures/events/continue.png")
        common.key_press("enter")

    if common.element_exist("pictures/events/gain_check.png"): #Pass to gain an EGO Gift
        logger.debug("Pass to gain EGO Gift")
        common.click_matching("pictures/events/gain_check.png")
        common.click_matching("pictures/events/proceed.png")
        skill_check()

    if common.element_exist("pictures/events/gain_gift.png"): #Proceed to gain
        logger.debug("Proceed to gain EGO Gift")
        common.click_matching("pictures/events/gain_gift.png")
        common.wait_skip("pictures/events/proceed.png")
        if common.element_exist("pictures/events/skip.png"):
            common.click_skip(4)
            event_choice()
    
    if common.element_exist("pictures/events/win_battle.png"): #Win battle to gain
        logger.debug("Win battle to gain EGO Gift")
        common.click_matching("pictures/events/win_battle.png")
        common.wait_skip("pictures/events/commence_battle.png")

    #special_events()

#def special_events():
#    if common.element_exist("mirror/events/kqe.png"):
#        common.click_matching("mirror/events/kqe.png")
#        common.wait_skip("pictures/events/continue.png")

def victory():
    logger.info("Run Won")
    common.click_matching("pictures/general/beeg_confirm.png")
    common.click_matching("pictures/general/claim_rewards.png")
    common.click_matching("pictures/general/md_claim.png")
    if common.element_exist("pictures/general/confirm_w.png"):
        logger.info("Rewards Claimed")
        common.click_matching("pictures/general/confirm_w.png")
        common.click_matching("pictures/general/confirm_b.png")
        check_loading()
    else: #incase not enough modules
        common.click_matching("pictures/general/to_window.png")
        common.click_matching("pictures/general/confirm_w.png")
        check_loading()
        logger.info("You dont have enough modules to continue")
        exit() 

def defeat():
    logger.info("Run Lost")
    common.click_matching("pictures/general/beeg_confirm.png")
    common.click_matching("pictures/general/claim_rewards.png")
    common.click_matching("pictures/general/give_up.png")
    common.click_matching("pictures/general/confirm_w.png")
    check_loading()