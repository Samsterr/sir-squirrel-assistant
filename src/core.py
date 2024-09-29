from src import common

def refill_enkephalin():
    common.click_matching("pictures/refresh/module.png")
    common.click_matching("pictures/refresh/right_arrow.png")
    common.click_matching("pictures/refresh/confirm.png")
    common.click_matching("pictures/navigating/window.png")

def navigate_to_md():
    common.click_matching("pictures/navigating/window.png")
    common.click_matching("pictures/navigating/drive.png")
    common.click_matching("pictures/navigating/MD.png")
    
