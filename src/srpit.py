import pyautogui
import pygetwindow as gw
from time import sleep
from PIL import Image
import numpy as np
from super_image import MsrnModel, ImageLoader
import os
import traceback
from global_variables import OFFSET_IMAGE


def combine_multuple_screenshots_into_one(images, n):
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    sum_height = sum(heights)
    new_image = Image.new('RGB', (max_width, sum_height))
    y_offset = 0
    for im in images:
        new_image.paste(im, (0, y_offset))
        y_offset += im.size[1]
    path = r".\screen_shots\screen-{}.jpg".format(n)
    new_image.save(path)


def move_to_coordinates_from_image(image_path, offset=[0, 0]):
    x, y = offset
    information = pyautogui.locateOnScreen(image_path, confidence=0.99)
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
    sleep(0.5)
    move_to_coordinates_from_image('./find_buttons/e-book2.png', [20, 20])
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
    else:
        return


def click_minimaze(reapet=1):
    if reapet == 10:
        return click_maximaze()
    try:
        move_to_coordinates_from_image(
            './find_buttons/minimaze_win_nutton.png', [55, 55])
        pyautogui.click()
    except Exception as e:
        click_minimaze(reapet=reapet+1)
    else:
        return


def click_mode_single_page():
    sleep(0.5)
    move_to_coordinates_from_image(
        './find_buttons/one_page_mode.png', [10, 10])
    pyautogui.doubleClick()


def check_if_bad_scroll_bar_showing():
    try:
        sleep(0.5)
        i = pyautogui.locateOnScreen(
            './find_buttons/scrollbar_bad.png', confidence=0.99)
        if i == None:
            raise Exception("Scroll bar is not showing")
    except Exception as e:
        return
    click_minimaze()
    click_maximaze()
    sleep(0.5)
    print("Bad scroll bar is showing")
    pyautogui.scroll(1736)
    check_if_bad_scroll_bar_showing()


def get_screenshot(n: int, ia=False, first=False, reapet=1):
    global OFFSET_IMAGE
    if reapet == 10:
        print("Big Error!, reapet for ten times without success")
        return "error"
    if first:
        click_maximaze()
        sleep(5)
        check_if_bad_scroll_bar_showing()
        move_to_coordinates_from_image(
            './find_buttons/next_page_button1.png', [-10, -100])
    else:
        click_minimaze()
        click_maximaze()
        check_if_bad_scroll_bar_showing()
        move_to_coordinates_from_image(
            './find_buttons/next_page_button1.png', [-10, -100])
        pyautogui.scroll(1736)
    sleep(0.4)
    images = get_all_3_screenshots(first)
    sleep(0.4)
    if images == "error":
        print("Error in get_screenshot", images)
        pyautogui.scroll(1736)
        return get_screenshot(n, reapet=reapet+1)
    img1, img2, img3 = images
    combine_multuple_screenshots_into_one([img1, img2, img3], n)
    if ia:
        image_file = Image.open(path)
        model = MsrnModel.from_pretrained('eugenesiow/msrn', scale=4)
        inputs = ImageLoader.load_image(image_file)
        preds = model(inputs)
        os.remove(path)
        ImageLoader.save_image(
            preds, r".\screen_shots\screenshots-{}.jpg".format(n))
        ImageLoader.save_compare(inputs, preds, path_to_save)


def click_next_page():
    sleep(0.5)
    move_to_coordinates_from_image(
        './find_buttons/next_page_button1.png', [0, 0])
    pyautogui.click()


def get_all_3_screenshots(first=False):
    global OFFSET_IMAGE
    img1, img2, img3 = 0, 0, 0
    try:
        sleep(0.3)
        img1 = pyautogui.screenshot(region=(55, 115, 1705, 905))
        pyautogui.scroll(-868)
        sleep(0.3)
        img2 = pyautogui.screenshot(region=(55, 115, 1705, 905))
        sleep(0.3)
        offsetLineImage = pyautogui.screenshot(
            region=(55, 900-OFFSET_IMAGE, 1705, 120+OFFSET_IMAGE))
        sleep(0.3)
        pyautogui.scroll(-868)
        information = pyautogui.locateOnScreen(
            offsetLineImage, confidence=0.99)
        sleep(0.3)
        img3 = pyautogui.screenshot(
            region=(55, information[1]+information[3], 1705, 905-information[1]))
        sleep(0.3)
        if img1 == None or img2 == None or img3 == None:
            raise Exception("Error")
    except TypeError as e:
        print("TypeError")
        if first:
            OFFSET_IMAGE = OFFSET_IMAGE - 50
        return "error"
    except ValueError as e:
        print("ValueError: ", e)
        if first:
            OFFSET_IMAGE = OFFSET_IMAGE + 50
        return "error"
    except Exception as e:
        print("Error: ", e, type(e))
        return "error"
    else:
        return [img1, img2, img3]
