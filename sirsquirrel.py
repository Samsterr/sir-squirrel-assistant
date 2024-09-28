from src import core, mirror
from pynput.mouse import Controller

mouse = Controller()
state = ""
run = 0

with open("gift_selection.txt","r") as f:
    gift = f.read().lower()

#core.refill_enkephalin(mouse)
core.navigate_to_md(mouse)
state = mirror.start_mirror(mouse,state)

if state == "GIFT_SELECT":
    gift = mirror.gift_choice(gift)
    if gift is None:
        gift = "pictures/mirror/gifts/random.png"
    state = mirror.gift_selection(mouse,gift,state)