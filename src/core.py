from src import common

def refill_enkephalin(mouse):
    common.click_matching(mouse, "pictures/refresh/module.png")
    common.click_matching(mouse, "pictures/refresh/right_arrow.png")
    common.click_matching(mouse, "pictures/refresh/confirm.png")
    common.click_matching(mouse, "pictures/refresh/window.png")

def navigate_to_md(mouse):
    common.click_matching(mouse,"pictures/navigating/window.png")
    common.click_matching(mouse,"pictures/navigating/drive.png")
    common.click_matching(mouse,"pictures/navigating/MD.png")
    
