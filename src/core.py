from src import common
import logging

logger = logging.getLogger(__name__)

def refill_enkephalin():
    """Converts to Module (Runs from the main menu)"""
    logger.info("Converting Enkephalin to Modules")
    common.click_matching("pictures/general/module.png")
    common.click_matching("pictures/general/right_arrow.png")
    common.click_matching("pictures/general/confirm_w.png")
    common.click_matching("pictures/general/cancel.png")

def navigate_to_md():
    """Navigates to the Mirror Dungeon from the menu"""
    logger.info("Navigating to Mirror Dungeon")
    common.click_matching("pictures/general/window.png")
    common.click_matching("pictures/general/drive.png")
    common.click_matching("pictures/general/MD.png")

def md_setup():
    if common.element_exist("pictures/mirror/general/md.png"):
        return
    else:
        refill_enkephalin()
        navigate_to_md()

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

def post_run_load():
    """There is some oddity in the loading time for this that makes it annoying to measure so this is a blanket wait for main menu stall"""
    while(not common.element_exist("pictures/general/module.png")):
        common.sleep(1)
    logger.info("Loaded back to Main Menu")

def reconnect():
    while(common.element_exist("pictures/general/server_error.png")):
        common.sleep(6)
        common.click_matching("pictures/general/retry.png")
        common.mouse_move(200,200)
    if common.element_exist("pictures/general/no_op.png"):
        common.click_matching("pictures/general/close.png")
        logger.info("COULD NOT RECONNECT TO THE SERVER. SHUTTING DOWN!")
        exit()
    logger.info("Reconnected")
    
def battle():
    """Handles battles by mashing winrate, also handles skill checks and end of battle loading"""
    logger.info("Starting Battle")
    battle_finished = 0
    while(battle_finished != 1):
        if common.element_exist("pictures/general/loading.png"): #Checks for loading screen to end the while loop
            logger.info("Loading")
            battle_finished = 1
            common.sleep(3)
        if common.element_exist("pictures/events/skip.png"): #Checks for special battle skill checks prompt then calls skill check functions
            while(True):
                common.click_skip(1)
                if common.element_exist("pictures/mirror/general/event.png"):
                    battle_check()
                    break
                if common.element_exist("pictures/events/skill_check.png"):
                    skill_check()
                    break
        if common.element_exist("pictures/battle/winrate.png"):
            x,y = common.uniform_scale_coordinates(2165,1343)
            common.mouse_move_click(x,y)
            common.key_press("p") #win rate keyboard key
            common.key_press("enter") #Battle Start key
        if common.element_exist("pictures/general/server_error.png"):
            logger.info("Lost Connection to Server, Reconnecting")
            reconnect()
    
def battle_check(): #pink shoes, woppily, doomsday clock
    logger.info("Battle Event Check")
    common.sleep(1)
    if common.element_exist("pictures/battle/investigate.png"): #Woppily
        logger.debug("WOPPILY")
        common.click_matching("pictures/battle/investigate.png")
        common.wait_skip("pictures/events/continue.png")
        return 0
        
    if common.element_exist("pictures/battle/NO.png"): #Woppily
        logger.debug("WOPPILY PT2")
        for i in range(3):
            common.click_matching("pictures/battle/NO.png")
            common.mouse_move_click(common.scale_x(1193),common.scale_y(623))
            while(not common.element_exist("pictures/events/proceed.png")):
                if common.element_exist("pictures/events/continue.png"):
                    common.click_matching("pictures/events/continue.png")
                    return 0
                common.mouse_click()
            common.click_matching("pictures/events/proceed.png")
            common.mouse_move_click(common.scale_x(1193),common.scale_y(623))
            while(not common.element_exist("pictures/battle/NO.png")):
                common.mouse_click()

    if common.element_exist("pictures/battle/refuse.png"): # Pink Shoes
        logger.debug("PINK SHOES")
        common.click_matching("pictures/battle/refuse.png")
        common.wait_skip("pictures/events/proceed.png")
        skill_check()
        return 0
    
    if common.element_exist("pictures/battle/offer_sinner.png"): #Doomsday Clock
        logger.debug("DOOMSDAY CLOCK")
        found = common.match_image("pictures/battle/offer_clay.png")
        if found:
            x,y = found[0]
            logger.debug("Found Clay Option")
            if common.luminence(x,y+common.scale_y(21)) > 24: #Test 1440 Values
                logger.debug("Offer CLAY USED")
                common.click_matching("pictures/battle/offer_clay.png")
                common.wait_skip("pictures/events/continue.png")
                return 0

        logger.debug("Using Sinner")
        common.click_matching("pictures/battle/offer_sinner.png")
        common.wait_skip("pictures/events/proceed.png")
        skill_check()
        return 0
        
    return 1

def skill_check():
    """Handles Skill checks in the game"""
    logger.info("Skill Check")
    check_images = [
        "pictures/events/very_high.png",
        "pictures/events/high.png",
        "pictures/events/normal.png",
        "pictures/events/low.png",
        "pictures/events/very_low.png"
        ] #Images for the skill check difficulties
    
    common.wait_skip("pictures/events/skill_check.png")
    common.sleep(1) #for the full list to render
    for i in check_images: #Choose the highest to pass check
        if common.element_exist(i,0.9):
            common.click_matching(i)
            logger.debug("Selected Skill Checker")
            break

    common.click_matching("pictures/events/commence.png")
    common.sleep(4) #Waits for coin tosses
    logger.debug("Coin tosses finished")
    common.mouse_move_click(common.scale_x(1193),common.scale_y(623))
    while(True):
        common.mouse_click()
        if common.element_exist("pictures/events/proceed.png"):
            common.click_matching("pictures/events/proceed.png")
            break
        if common.element_exist("pictures/events/continue.png"):
            common.click_matching("pictures/events/continue.png")
            break
    logger.debug("Finished Skill check")

    if common.element_exist("pictures/events/skip.png"):
        logger.debug("DEBUG: NOON OF VIOLET")
        common.wait_skip("pictures/battle/violet_hp.png")
        common.wait_skip("pictures/events/continue.png")

    else:
        common.sleep(1) #in the event of ego gifts
        if common.element_exist("pictures/mirror/general/ego_gift_get.png"):
            common.click_matching("pictures/general/confirm_b.png")
            logger.debug("DEBUG: EGO Gift prompt")