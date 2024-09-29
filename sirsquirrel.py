from src import core, mirror

state = ""
run = 0
initial_gift_coords = [420,580,740]

with open("gift_selection.txt","r") as f:
    gift = f.read().lower()

#core.refill_enkephalin()
core.navigate_to_md()
state = mirror.start_mirror(state)

if state == "GIFT_SELECT":
    if gift == "sinking":
        initial_gift_coords.pop(0)
    else:
        initial_gift_coords.pop(2)
    gift = mirror.gift_choice(gift)
    if gift is None:
        gift = "pictures/mirror/gifts/random.png"
    state = mirror.gift_selection(gift,state,initial_gift_coords)