import pyautogui
import pygetwindow as gw
from time import sleep
from PIL import Image, ImageGrab, ImageDraw
from pytesseract import pytesseract
import numpy as np
import os
import traceback
OFFSET_IMAGE = 50
ERRORS = 0

executable_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pytesseract.tesseract_cmd = executable_tesseract


def get_page():
    bbox = (60, 1030, 190, 1070)
    im = ImageGrab.grab(bbox)
    text = pytesseract.image_to_string(im)
    print(text)
    return text


def combine_multuple_screenshots_into_one(images, n):
    widths, height = zip(*(i.size for i in images))
    max_width = max(widths)
    sum_height = sum(height)
    new_image = Image.new('RGB', (max_width, sum_height))
    y_offset = 0
    for im in images:
        new_image.paste(im, (0, y_offset))
        y_offset += im.size[1]
    path = r".\screen_shots\screen-{}.jpg".format(n)
    new_image.save(path, quality=100)


def move_to_coordinates_from_image(image_path, offset=[0, 0]):
    x, y = offset
    information = pyautogui.locateOnScreen(image_path, confidence=0.95)
    if information == None:
        print("error in move_to_coordinates_from_image")
        raise TypeError("button not found in image")
    informationX = information[0]
    informationY = information[1]
    pyautogui.moveTo(informationX+x, informationY+y, duration=0.2,
                     tween=pyautogui.easeInOutQuad)


def move_b_smart():
    codeWindow = 0
    all_win = gw.getAllTitles()
    for win in all_win:
        if win.startswith("My"):
            codeWindow = win
            break
    win = gw.getWindowsWithTitle(codeWindow)[0]
    win.activate()
    sleep(1)


def move_to_code():
    win = gw.getWindowsWithTitle(find_code_window())[0]
    win.activate()


def find_code_window():
    codeWindow = 0
    all_win = gw.getAllTitles()
    for win in all_win:
        if win.startswith("main.py"):
            codeWindow = win
            break
    return codeWindow


def click_e_book():
    move_to_coordinates_from_image('./find_buttons/e-book.png', [20, 20])
    pyautogui.click()


def click_maximaze(reapet=1):
    if reapet == 10:
        return click_minimaze()
    try:
        move_to_coordinates_from_image(
            './find_buttons/maximaze_win_button.png', [55, 55])
        pyautogui.click()
    except Exception as e:
        click_maximaze(reapet=reapet+1)


def click_minimaze(reapet=1):
    if reapet == 10:
        return click_maximaze()
    try:
        move_to_coordinates_from_image(
            './find_buttons/minimaze_win_nutton.png', [55, 55])
        pyautogui.click()
    except Exception as e:
        click_minimaze(reapet=reapet+1)


def click_mode_single_page():
    try:
        move_to_coordinates_from_image(
            './find_buttons/one_page_mode.png', [10, 10])
        pyautogui.doubleClick()
    except Exception as e:
        click_mode_single_page()
    else:
        return


def check_if_bad_scroll_bar_showing():
    try:

        i = pyautogui.locateOnScreen(
            './find_buttons/scrollbar_bad.png', confidence=0.99)
        if i == None:
            raise Exception("Scroll bar is not showing")
    except Exception as e:
        return
    click_minimaze()
    click_maximaze()
    pyautogui.scroll(1736)
    check_if_bad_scroll_bar_showing()


def check_if_scrollbar_side_is_on_top():
    color = pyautogui.pixel(1827, 106)
    if color[0] >= 235 and color[1] >= 235 and color[2] >= 235:
        return False
    return True


def check_if_two_scroll_are_enough():
    color = pyautogui.pixel(1830-1, 990-1)
    if color[0] >= 235 and color[1] >= 235 and color[2] >= 235:
        return False
    return True


def check_if_is_blank_page(region=(50, 85, 1690, 1024-100), color=247):
    img = pyautogui.screenshot(region=region)
    data = img.getdata()
    data = list(data)
    value = True
    for i, val in enumerate(data):
        if i >= len(data)-2:
            break
        condition = val[0] >= color and val[1] >= color and val[2] >= color
        if condition:
            continue
        value = False
        break
    return value


def initialize_get_screenshot(first):
    if first:
        click_maximaze()
        sleep(1)
        check_if_bad_scroll_bar_showing()
    else:
        click_minimaze()
        click_maximaze()
        check_if_bad_scroll_bar_showing()
        pyautogui.scroll(1736)


def click_next_page():
    sleep(0.2)
    move_to_coordinates_from_image(
        './find_buttons/next_page_button1.png', [0, 0])
    pyautogui.click()


def get_2_screens(img1, offsetLineImage):
    information = pyautogui.locateOnScreen(offsetLineImage)
    img2, null = get_screenshot_with_offset(information)
    os.remove("./find_buttons/offset.png")
    return [img1, img2]


def get_each_screenshot(position, scroll=False):
    try:
        sleep(0.1)
        img = pyautogui.screenshot(region=position)
        if scroll:
            pyautogui.scroll(-868)
        return img
    except:
        raise Exception("error in get_each_screenshot")


def get_all_3_screenshots(n, first=False):
    global OFFSET_IMAGE, ERRORS
    img1, img2, img3 = 0, 0, 0
    try:
        if check_if_is_blank_page():
            return "continue"
        img1 = get_each_screenshot((0, 115, 1815, 905))
        check_if_bad_scroll_bar_showing()
        if check_if_scrollbar_side_is_on_top():
            img1 = get_each_screenshot((0, 115, 1815, 905))
        img1 = get_each_screenshot((0, 115, 1815, 905))
        offsetLineImage_for_two = get_each_screenshot(
            (50, 900-OFFSET_IMAGE, 1815 - 100, (120+OFFSET_IMAGE)), True)
        img1 = clear_from_buttons(img1)

        img2 = get_each_screenshot((0, 115, 1815, 905))
        offsetLineImage = get_each_screenshot(
            (50, 900-OFFSET_IMAGE, 1815 - 100, 120+OFFSET_IMAGE))

        if check_if_two_scroll_are_enough():
            offsetLineImage_for_two.save("./find_buttons/offset.png")
            return get_2_screens(img1, offsetLineImage_for_two)
        img2 = clear_from_buttons(img2)
        pyautogui.scroll(-868)

        bbox_of_blank_page = (50, 85, 1690, 1024-250)
        if check_if_is_blank_page(bbox_of_blank_page):
            if n == 0:
                return "continue"
            before_img = Image.open(f"./screen_shots/screen-{n-1}.jpg")
            distance_remain = before_img.size[1] - \
                (img1.size[1] + img2.size[1])
            img3 = get_each_screenshot(
                (0, (1024 - 5) - distance_remain, 1815, distance_remain))
            img3 = clear_from_buttons(img3, offsetLineImage.size[1])
            return [img1, img2, img3]

        information = pyautogui.locateOnScreen(
            offsetLineImage, confidence=0.99)
        offsetLineImage.save("./find_buttons/offset.png")
        img3, offset_height = get_screenshot_with_offset(information)
        img3 = clear_from_buttons(img3, offset_height)

        if img1 == None or img2 == None or img3 == None:
            raise Exception("Error")

        return [img1, img2, img3]
    except TypeError as e:
        print("TypeError ", e, OFFSET_IMAGE)
        print(traceback.format_exc())
        ERRORS += 1

        if first:
            OFFSET_IMAGE += 50
        return "error"
    except ValueError as e:
        print("ValueError: ", e, OFFSET_IMAGE)
        print(traceback.format_exc())

        if first:
            if OFFSET_IMAGE <= 10:
                OFFSET_IMAGE += 50
            else:
                OFFSET_IMAGE -= 50

        return "error"
    except Exception as e:
        print("Error: ", e, type(e))
        print(traceback.format_exc())
        return "error"
    else:
        return [img1, img2, img3]


def get_screenshot_with_offset(offset=None, times=0):
    global OFFSET_IMAGE
    offset_aument = 0
    img = None
    try:
        if times > 0 or offset == None:
            pyautogui.scroll(1736)
            pyautogui.scroll(-868)
            img_offset = get_each_screenshot(
                (50, 900-OFFSET_IMAGE, 1815 - 100, 120+OFFSET_IMAGE))
            pyautogui.scroll(-868)
            offset = pyautogui.locateOnScreen(
                img_offset, confidence=0.99)
            img_offset.save("./find_buttons/offset.png")

        y = 1024
        h = (y - 5) - (offset[1]+offset[3])
        img = get_each_screenshot((0, offset[1]+offset[3], 1815, h))
        return (img, offset[3])
    except TypeError:
        offset_aument += 30
        OFFSET_IMAGE += 30
        img, offset_height = get_screenshot_with_offset(offset, times=1+times)
        return (img, offset_height)


def clear_from_buttons(img, offset_height=None):
    width, height = img.size
    initial_height = round(height / 2)
    if offset_height != None:
        initial_height = (round(height / 2) - offset_height) - 7
    initial_height = initial_height - 87
    left_bbox = (0, initial_height, 48, height-initial_height-54)
    img = clear_button(left_bbox, img)
    right_bbox = (width-30, initial_height, width, height-initial_height-54)
    img = clear_button(right_bbox, img)
    return img


def clear_button(bbox, img):
    crop = img.crop(bbox)
    new_img = remove_image(crop)
    back_im = img.copy()
    back_im.paste(new_img, (bbox[0], bbox[1]))
    return back_im


def remove_image(im):
    width, height = im.size
    rgb = im.getpixel((width-5, 1))
    return Image.new(mode="RGB", size=(width, height), color=(rgb[0], rgb[1], rgb[2]))


def get_screenshot(n: int, first=False, reapet=1):
    global OFFSET_IMAGE
    if reapet == 10:
        print("Big Error!, reapet for ten times without success")
        return "error"
    initialize_get_screenshot(first)
    images = get_all_3_screenshots(n, first)
    if len(images) == 2:
        return combine_multuple_screenshots_into_one(images, n)
    if images == "error":
        print("Error in get_screenshot", images)
        pyautogui.scroll(1736)
        return get_screenshot(n, reapet=reapet+1)
    elif images == "continue":
        return "continue"
    img1, img2, img3 = images
    combine_multuple_screenshots_into_one([img1, img2, img3], n)
    return "success"
