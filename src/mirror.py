from src import common

def start_mirror(mouse, state):
    if common.element_exist("pictures/mirror/entrance/in_progress.png"): #check if MD is in Progress
        common.click_matching(mouse,"pictures/mirror/entrance/in_progress.png")
        common.click_matching(mouse, "pictures/mirror/entrance/resume.png")
        if common.element_exist("pictures/mirror/entrance/gift_select.png"): #Checks if in gift select
            state = "GIFT_SELECT"
            return state
        if common.element_exist("pictures/mirror/entrance/squad_select.png"): #checks if in Squad select
            state = "SQUAD_SELECT"
            return state
        state = "NAVIGATING" #If not its still navigating
        return state

    common.click_matching(mouse,"pictures/mirror/entrance/normal.png")
    common.click_matching(mouse,"pictures/mirror/entrance/enter.png")
    #Checks for Wish of Stars
    if common.element_exist("pictures/mirror/entrance/wish.png"):
        common.click_matching(mouse,"pictures/mirror/entrance/wish_confirm.png")
    state = "GIFT_SELECT"
    return state
    
def gift_choice(gift):
    match gift:
        case "sinking":
            return "pictures/mirror/gifts/sinking.png"
        case "bleed":
            return "pictures/mirror/gifts/bleed.png"
        case "burn":
            return "pictures/mirror/gifts/burn.png"
        case "charge":
            return "pictures/mirror/gifts/charge.png"        
        case "poise":
            return "pictures/mirror/gifts/poise.png"
        case "rupture":
            return "pictures/mirror/gifts/rupture.png"
        case "tremor":
            return "pictures/mirror/gifts/tremor.png"
        case "slash":
            return "pictures/mirror/gifts/slash.png"
        case "pierce":
            return "pictures/mirror/gifts/pierce.png"
        case "blunt":
            return "pictures/mirror/gifts/blunt.png"
        case "random":
            return "pictures/mirror/gifts/random.png"
        
def gift_selection(mouse,gift,state):
    return