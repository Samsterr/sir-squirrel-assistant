from src import common

def refill_enkephalin():
    """Refills enkephalin (Runs from the main menu)"""
    common.click_matching("pictures/general/module.png")
    common.click_matching("pictures/general/right_arrow.png")
    common.click_matching("pictures/general/confirm_w.png")
    common.click_matching("pictures/general/window.png")

def navigate_to_md():
    """Navigates to the Mirror Dungeon from the menu"""
    common.click_matching("pictures/general/window.png")
    common.click_matching("pictures/general/drive.png")
    common.click_matching("pictures/general/MD.png")

def battle():
    """Handles battles by mashing winrate, also handles skill checks and end of battle loading"""
    battle_finished = 0
    while(battle_finished != 1):
        if common.element_exist("pictures/general/loading.png"): #Checks for loading screen to end the while loop
            battle_finished = 1
            common.sleep(3)
        if common.element_exist("pictures/events/skip.png"): #Checks for skill checks prompt then calls skill check function
            skill_check()
        if common.element_exist("pictures/battle/start.png"):
            common.sleep(1)
            common.mouse_move_click(1150,640) #handle onscreen prompts example sinking wolf
            common.key_press("p") #win rate keyboard key
            common.key_press("enter") #Battle Start key
    
def skill_check(): #need to touch up, very rough
    """Handles Skill checks in the game"""
    check_images = [
        "pictures/events/very_high.png",
        "pictures/events/high.png",
        "pictures/events/normal.png",
        "pictures/events/low.png",
        "pictures/events/very_low.png"
        ] #Images for the skill check difficulties
    
    #common.click_matching("pictures/events/proceed.png")
    common.click_matching("pictures/events/skip.png") #mash skip to get the ui to show
    while(not common.element_exist("pictures/events/skill_check.png")):
        common.mouse_click()

    common.sleep(1)
    for i in check_images: #Choose the highest to pass check
        if common.element_exist(i,0.9):
            common.click_matching(i)
            common.sleep(1)
            break

    common.click_matching("pictures/events/commence.png")
    common.sleep(5) #Waits for coin tosses
    common.click_matching("pictures/events/skip.png")
    while(not common.element_exist("pictures/events/continue.png")):
        #common.click_matching("pictures/events/skip.png")
        common.mouse_click()
    common.click_matching("pictures/events/continue.png")
    common.sleep(1)
    if common.element_exist("pictures/mirror/general/ego_gift_get.png"):
        common.key_press("enter")
        #common.click_matching("pictures/general/confirm_b.png")
    #Need to consider gaining ego gift here
