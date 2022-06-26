import pyautogui
import pygetwindow as gw
from time import sleep
from PIL import Image
import numpy as np
from super_image import MsrnModel, ImageLoader
import os


def move_to_coordinates_from_image(image_path, offset=[0, 0]):
    x, y = offset
    information = pyautogui.locateOnScreen(image_path, confidence=0.99)
    informationX = information[0]
    informationY = information[1]
    pyautogui.moveTo(informationX+x, informationY+y, duration=1,
                     tween=pyautogui.easeInOutQuad)


def move_b_smart():
    codeWindow = 0
    all_win = gw.getAllTitles()
    for win in all_win:
        if win.startswith("My"):
            codeWindow = win
            break
    win = gw.getWindowsWithTitle(codeWindow)[0]
    print(codeWindow)
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


def get_pages():
    sleep(0.5)
    move_to_coordinates_from_image('./find_buttons/e-book.png', [780, 200])
    pyautogui.click()
    pyautogui.moveTo(647, 471, duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.doubleClick()
    pyautogui.hotkey('ctrl', 'c')


def write_pages_on_file():
    sleep(0.5)
    move_to_coordinates_from_image('./find_buttons/find_txt.png')
    pyautogui.click()
    pyautogui.moveTo(1000, 170, duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    for i in range(40):
        pyautogui.press('backspace')
    pyautogui.hotkey('ctrl', 'v')


def close_popup():
    sleep(0.5)
    move_to_coordinates_from_image('./find_buttons/find_close_pupup.png')
    pyautogui.click()


def click_e_book():
    sleep(0.5)
    move_to_coordinates_from_image('./find_buttons/e-book.png', [20, 20])
    pyautogui.click()


def click_maximaze():
    sleep(0.5)
    move_to_coordinates_from_image(
        './find_buttons/maximaze_win_button.png', [20, 20])
    pyautogui.click()


def click_mode_single_page():
    sleep(0.5)
    move_to_coordinates_from_image(
        './find_buttons/one_page_mode.png', [10, 10])
    pyautogui.doubleClick()


def get_screenshot(n: int, ia=False):

    im = pyautogui.screenshot(region=(565, 80, 705, 940))
    path = r".\screen_shots\screen-{}.jpg".format(n)
    path_to_save = r".\screen_shots\screenshot-{}.jpg".format(n)
    im.save(path, "JPEG")
    if ia:
        image_file = Image.open(path)
        model = MsrnModel.from_pretrained('eugenesiow/msrn', scale=4)
        inputs = ImageLoader.load_image(image_file)
        preds = model(inputs)
        os.remove(path)
        ImageLoader.save_image(
            preds, r".\screen_shots\screenshots-{}.jpeg".format(n))
        ImageLoader.save_compare(inputs, preds, path_to_save)


def click_next_page():
    sleep(0.5)
    move_to_coordinates_from_image(
        './find_buttons/next_page_button.png', [30, 70])
    pyautogui.click()


def main():
    move_b_smart()
    get_pages()
    move_to_code()
    write_pages_on_file()
    sleep(1)
