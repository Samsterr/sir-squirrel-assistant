import numpy as np
import cv2
import time
from mss import mss
import pyautogui
import json
import secrets

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
    """Captures the screen using MSS and converts it to a numpy array for CV2"""
    with mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        #output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

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


def debug_match_image(template_path ,threshold=0.8):
    """Same as match_image but draws the rectangle around found element"""
    screenshot = capture_screen()
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template image '{template_path}' not found.")
    template_height, template_width = template.shape[:2]

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Get locations where the match confidence exceeds the threshold
    locations = np.where(result >= threshold)
    boxes = []
    # List to hold the center coordinates of all detected elements
    found_elements = []

    # Loop through all the matching locations
    for pt in zip(*locations[::-1]):  # Switch columns and rows
        top_left = pt
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        boxes.append([top_left[0], top_left[1], bottom_right[0], bottom_right[1]])


    boxes = np.array(boxes)

    # Apply non-maximum suppression to remove overlapping boxes
    filtered_boxes = non_max_suppression_fast(boxes)

    # List to hold the center coordinates of all filtered elements
    found_elements = []

    # Draw the filtered boxes and calculate center points
    for (x1, y1, x2, y2) in filtered_boxes:
        # Draw a rectangle around the filtered element
        cv2.rectangle(screenshot, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

        # Calculate the center of the found element
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Add the center coordinates to the list
        found_elements.append((center_x, center_y))

    # Display the screenshot with rectangles drawn around the detected elements
    cv2.imshow('Detected Elements', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Return the list of center coordinates of all found elements or None if no elements found
    if len(found_elements) == 0:
        return None
    
    return found_elements

def match_image(template_path ,threshold=0.8):
    """Finds the image specified and returns the centre coordinates"""
    screenshot = capture_screen()
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template image '{template_path}' not found.")
    template_height, template_width = template.shape[:2]

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Get locations where the match confidence exceeds the threshold
    locations = np.where(result >= threshold)
    boxes = []

    found_elements = []

    # Loop through all the matching locations
    for pt in zip(*locations[::-1]):  # Switch columns and rows
        top_left = pt
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        boxes.append([top_left[0], top_left[1], bottom_right[0], bottom_right[1]])

    boxes = np.array(boxes)

    # Apply non-maximum suppression to remove overlapping boxes
    filtered_boxes = non_max_suppression_fast(boxes)

    # List to hold the center coordinates of all filtered elements
    found_elements = []

    # Draw the filtered boxes and calculate center points
    for (x1, y1, x2, y2) in filtered_boxes:
        # Draw a rectangle around the filtered element
        #cv2.rectangle(screenshot, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

        # Calculate the center of the found element
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Add the center coordinates to the list
        found_elements.append((center_x, center_y))

    # Return the list of center coordinates of all found elements or None if no elements found
    if len(found_elements) == 0:
        return None
    
    return found_elements

def click_skip(times):
    """Click Skip the amount of time specified"""
    click_matching("pictures/events/skip.png")
    for i in range(times):
        mouse_click()

def wait_skip(img_path, threshold=0.8):
    click_matching("pictures/events/skip.png")
    while(not element_exist(img_path,threshold)):
        mouse_click()
    click_matching(img_path,threshold)

def wait_click(image_path,threshold=0.8):
    """Waits for an image to match and click centre of the image"""
    while(not match_image(image_path,threshold)):
        sleep(1)
    click_matching(image_path,threshold)

def click_matching(image_path,threshold=0.8):
    if element_exist(image_path):
        found = match_image(image_path,threshold)
        x,y = found[0]
        mouse_move_click(x,y)
        time.sleep(1)
        
def press_matching(key,image_path):
    """Waits for an image to match and presses a key"""
    found = match_image(image_path)

    #Searches until Image Found if supposed to be found
    if found is None:
        time.sleep(3)
        press_matching(key,image_path)

    #if found, presses the key specified
    else:
        time.sleep(2)
        x,y = found[0]
        key_press(key)
        
#dk if i need this for element checking
def element_exist(img_path,threshold=0.8):
    """Checks if the element exists if not returns none"""
    return match_image(img_path,threshold)

def squad_order(status):
    """Returns a list of the image locations depending on the sinner order specified in the json file"""
    characters_positions = {
    "yisang": (435, 375),
    "faust": (635, 375),
    "donquixote": (835, 375),
    "ryoshu": (1035, 375),
    "meursault": (1235, 375),
    "honglu": (1435, 375),
    "heathcliff": (435, 675),
    "ishmael": (635, 675),
    "rodion": (835, 675),
    "sinclair": (1035, 675),
    "outis": (1235, 675),
    "gregor": (1435, 675)
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
                sinner_order.append(characters_positions[sinner_name])  
    return sinner_order

def luminence(x,y):
    """Get Luminence of the pixel and return overall coefficient"""
    screenshot = capture_screen()
    pixel_image = screenshot[y, x]
    coeff = (pixel_image[0] + pixel_image[1] + pixel_image[2]) / 3
    return coeff

def scale_match_image(template_path, threshold=0.8):
    """Finds the image specified and returns the center coordinates using multi-scale template matching."""
    screenshot = capture_screen()
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template image '{template_path}' not found.")
    
    template_height, template_width = template.shape[:2]

    # Parameters for multi-scale template matching
    scale_start = 0.5  # Start with a scale of 50% of the original template size
    scale_end = 1.5    # Go up to 150% of the original template size
    scale_step = 0.1   # Scale step size

    all_boxes = []

    for scale in np.arange(scale_start, scale_end, scale_step):
        # Resize the template image
        resized_template = cv2.resize(template, (int(template_width * scale), int(template_height * scale)))
        resized_height, resized_width = resized_template.shape[:2]

        # Perform template matching on the resized template
        result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)

        # Get locations where the match confidence exceeds the threshold
        locations = np.where(result >= threshold)

        # Loop through all the matching locations
        for pt in zip(*locations[::-1]):  # Switch columns and rows
            top_left = pt
            bottom_right = (top_left[0] + resized_width, top_left[1] + resized_height)
            all_boxes.append([top_left[0], top_left[1], bottom_right[0], bottom_right[1]])

    if len(all_boxes) == 0:
        return None  # No matches found

    all_boxes = np.array(all_boxes)

    # Apply non-maximum suppression to remove overlapping boxes
    filtered_boxes = non_max_suppression_fast(all_boxes)

    # List to hold the center coordinates of all filtered elements
    found_elements = []

    # Calculate the center points of the filtered boxes
    for (x1, y1, x2, y2) in filtered_boxes:
        # Calculate the center of the found element
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Add the center coordinates to the list
        found_elements.append((center_x, center_y))

    # Return the list of center coordinates of all found elements or None if no elements found
    return found_elements if found_elements else None
