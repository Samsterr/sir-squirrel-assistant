import numpy as np
import cv2
import time
from mss import mss
import pyautogui
import json
import os
import secrets
from mss.tools import to_png

pyautogui.FAILSAFE = False

def random_choice(list):
    return secrets.choice(list)

def sleep(x):
    """Sleep function"""
    time.sleep(x)

def mouse_scroll(amount):
    pyautogui.scroll(amount)

def mouse_move(x,y):
    """Moves the mouse to the X,Y coordinate specified"""
    pyautogui.moveTo(x,y)

def mouse_click():
    """Performs a left click on the current position"""
    pyautogui.click()

def mouse_hold():
    pyautogui.mouseDown()
    sleep(2)
    pyautogui.mouseUp()

def mouse_down():
    pyautogui.mouseDown()

def mouse_up():
    pyautogui.mouseUp()

def mouse_move_click(x,y):
    """Moves the mouse to the X,Y coordinate specified and performs a left click"""
    pyautogui.click(x,y)

def mouse_drag(x,y):
    """Drag from coordinates to the specified coords"""
    pyautogui.dragTo(x,y,1,button='left')

def key_press(Key, presses=1):
    """Presses the specified key X amount of times"""
    pyautogui.press(Key,presses)

def capture_screen():
    """Captures the full screen using MSS and converts it to a numpy array for CV2."""
    with mss() as sct:
        # Dynamically get the current screen resolution
        monitor = sct.monitors[1]  # [1] is the primary monitor; adjust if using multiple monitors
        
        # Capture the screen with the current resolution
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        
        # Convert the color from BGRA to BGR for OpenCV compatibility
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img

def save_match_screenshot(screenshot, top_left, bottom_right, template_path, match_index):
    """Saves a screenshot of the matched region, preserving directory structure in 'higher_res'."""
    # Crop the matched region from the full screenshot
    match_region = screenshot[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    # Create a modified output path in the 'higher_res' folder
    output_path = os.path.join("higher_res", template_path)
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a unique filename for each match within the higher_res directory
    output_path = os.path.splitext(output_path)[0]  # Remove original extension
    output_path = f"{output_path}.png"  # Append match index
    if os.path.exists(output_path):
        return
    # Save the cropped region
    cv2.imwrite(output_path, match_region)
    print(f"Match saved at {output_path}")

def match_image(template_path, threshold=0.8):
    """Finds the image specified and returns the center coordinates, regardless of screen resolution,
    and saves screenshots of each match found."""
    
    # Capture current screen and get dimensions
    screenshot = capture_screen()
    screenshot_height, screenshot_width = screenshot.shape[:2]

    # Calculate scale factor
    scale_factor_x = screenshot_width / 2560
    scale_factor_y = screenshot_height / 1440
    scale_factor = min(scale_factor_x,scale_factor_y)
    # Load and resize the template image according to the scale factor
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template image '{template_path}' not found.")
    
    template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    template_height, template_width = template.shape[:2]

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Get locations where the match confidence exceeds the threshold
    if scale_factor < 0.75:
        threshold = threshold-0.05 #Testing for detecting on lower scales
    locations = np.where(result >= threshold)
    boxes = []

    # Loop through all the matching locations and create bounding boxes
    for pt in zip(*locations[::-1]):  # Switch columns and rows
        top_left = pt
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        boxes.append([top_left[0], top_left[1], bottom_right[0], bottom_right[1]])

    boxes = np.array(boxes)

    # Apply non-maximum suppression to remove overlapping boxes
    filtered_boxes = non_max_suppression_fast(boxes)

    # List to hold the center coordinates of all filtered elements
    found_elements = []
    
    # Save a screenshot of each matched region
    for match_index, (x1, y1, x2, y2) in enumerate(filtered_boxes):
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        found_elements.append((center_x, center_y))
    
    if found_elements:
        #save_match_screenshot(screenshot, (x1, y1), (x2, y2), template_path, match_index)
        return sorted(found_elements)
    # Return the list of center coordinates of all found elements or None if no elements found
    return None

def proximity_check(list1, list2, threshold):
    close_pairs = set()  # To store pairs of coordinates that are close
    for coord1 in list1:
        for coord2 in list2:
            distance = np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
            if distance < threshold:
                close_pairs.add(coord1)
    return close_pairs

def debug_match_image(template_path, threshold=0.8):
    """Finds the image specified and returns the center coordinates, regardless of screen resolution,
       and draws rectangles on each match found."""
    
    # Capture current screen and get dimensions
    screenshot = capture_screen()
    screenshot_height, screenshot_width = screenshot.shape[:2]

    # Calculate scale factor
    scale_factor_x = screenshot_width / 2560
    scale_factor_y = screenshot_height / 1440
    scale_factor = min(scale_factor_x, scale_factor_y)
    
    # Load and resize the template image according to the scale factor
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template image '{template_path}' not found.")
    
    template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    template_height, template_width = template.shape[:2]

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Get locations where the match confidence exceeds the threshold
    locations = np.where(result >= threshold)
    boxes = []

    # Loop through all the matching locations and create bounding boxes
    for pt in zip(*locations[::-1]):  # Switch columns and rows
        top_left = pt
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        boxes.append([top_left[0], top_left[1], bottom_right[0], bottom_right[1]])

    boxes = np.array(boxes)

    # Apply non-maximum suppression to remove overlapping boxes
    filtered_boxes = non_max_suppression_fast(boxes)

    # List to hold the center coordinates of all filtered elements
    found_elements = []

    # Draw rectangles around each filtered match and calculate center coordinates
    for (x1, y1, x2, y2) in filtered_boxes:
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        found_elements.append((center_x, center_y))
        
        # Draw rectangle around the match
        cv2.rectangle(screenshot, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

    # Show the screenshot with rectangles for immediate feedback
    cv2.imshow("Matches", screenshot)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

    return found_elements if found_elements else None

def get_resolution():
    """Gets the current resolution"""
    return pyautogui.size()

def non_max_suppression_fast(boxes, overlapThresh=0.5):
    """Some stonks thing to remove multiple detections on the same position"""
    if len(boxes) == 0:
        return []

    # Convert to float if necessary
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # Initialize the list of picked indexes
    pick = []

    # Get coordinates of bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # Compute the area of the bounding boxes and sort by the bottom-right y-coordinate
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # Keep looping while some indexes still remain in the indexes list
    while len(idxs) > 0:
        # Grab the last index in the indexes list, add the index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # Find the largest (x, y) coordinates for the start of the bounding box
        # and the smallest (x, y) coordinates for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # Compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # Compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # Delete all indexes from the index list that have an overlap greater than the threshold
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    # Return only the bounding boxes that were picked
    return boxes[pick].astype("int")

def get_aspect_ratio():
    width,height = pyautogui.size()
    if (width / 4) * 3 == height:
        return "4:3"
    if (width / 16) * 9 == height:
        return "16:9"
    if (width / 16) * 10 == height:
        return "16:10"
    else:
        return None

def scale_x(x):
    width,height = get_resolution()
    scale_factor_x = width / 2560
    return round(x * scale_factor_x)

def scale_y(y):
    width,height = get_resolution()
    scale_factor_y =  height / 1440
    return round(y * scale_factor_y)

def uniform_scale_single(coord):
    width,height = get_resolution()
    scale_factor_x = width / 2560
    scale_factor_y = height / 1440
    scale_factor = min(scale_factor_x,scale_factor_y)
    return round(scale_factor * coord)

def uniform_scale_coordinates(x, y):
    """Scale (x, y) coordinates from 1080p to the current screen resolution."""
    width,height = get_resolution()
    scale_factor_x = width / 2560
    scale_factor_y = height / 1440
    scale_factor = min(scale_factor_x,scale_factor_y)
    scaled_x = round(x * scale_factor_x)
    scaled_y = round(y * scale_factor_y)
    return scaled_x, scaled_y

def click_skip(times):
    """Click Skip the amount of time specified"""
    mouse_move_click(scale_x(1193),scale_y(623))
    for i in range(times):
        mouse_click()

def wait_skip(img_path,threshold=0.8):
    """Clicks on the skip button and waits for specified element to appear"""
    mouse_move_click(scale_x(1193),scale_y(623))
    while(not element_exist(img_path,threshold)):
        mouse_click()
    click_matching(img_path,threshold)

def click_matching(image_path,threshold=0.8):
    if element_exist(image_path):
        found = match_image(image_path,threshold)
        if found:
            x,y = found[0]
            mouse_move_click(x,y)
            time.sleep(0.5)
    else:
        mouse_move(200,200)
        click_matching(image_path,threshold)

def element_exist(img_path,threshold=0.8):
    """Checks if the element exists if not returns none"""
    return match_image(img_path,threshold)

def squad_order(status):
    """Returns a list of the image locations depending on the sinner order specified in the json file"""
    characters_positions = {
    "yisang": (580, 500),
    "faust": (847, 500),
    "donquixote": (1113, 500),
    "ryoshu": (1380, 500),
    "meursault": (1647, 500),
    "honglu": (1913, 500),
    "heathcliff": (580, 900),
    "ishmael": (847, 900),
    "rodion": (1113, 900),
    "sinclair": (1380, 900),
    "outis": (1647, 900),
    "gregor": (1913, 900)
}

    with open("config/squad_order.json", "r") as f:
        squads = json.load(f)
    squad = squads[status]
    
    sinner_order = []
    for i in range(1,13):
      for name, value in squad.items():
        if value == i:
            sinner_name = name
            if sinner_name in characters_positions:
                position = characters_positions[sinner_name]
                x,y = characters_positions[sinner_name]
                sinner_order.append(uniform_scale_coordinates(x,y))  
    return sinner_order

def luminence(x,y):
    """Get Luminence of the pixel and return overall coefficient"""
    screenshot = capture_screen()
    pixel_image = screenshot[y, x]
    coeff = (int(pixel_image[0]) + int(pixel_image[1]) + int(pixel_image[2])) / 3
    return coeff

def error_screenshot():
    os.makedirs("error", exist_ok=True)
    with mss() as sct:
        # Dynamically get the current screen resolution
        monitor = sct.monitors[1]  # [1] is the primary monitor; adjust if using multiple monitors
        # Capture the screen with the current resolution
        screenshot = sct.grab(monitor)
        png = to_png(screenshot.rgb, screenshot.size)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        with open("error/" + timestamp + ".png", "wb") as f:
            f.write(png)