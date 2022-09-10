import pyautogui
from time import sleep
from PIL import ImageGrab
import os
import pyperclip
from pynput.keyboard import Listener, Key
from threading import Thread
import sys
import os

value = None


def on_release(key):
    if key == Key.enter:
        pyperclip.copy(value)


def clear(): return os.system('cls')


def get_color(position):
    bbox = (position.x, position.y, position.x+1, position.y+1)
    im = ImageGrab.grab(bbox)
    return list(im.getdata())[0]


def listener_function():
    with Listener(on_release=on_release) as listener:
        listener.join()


def current_position():
    try:
        global value
        thread = Thread(target=listener_function)
        thread.start()
        while True:
            position = pyautogui.position()
            color = get_color(position)
            value = f"{position}. color: {color}"
            print(value)
            clear()
    except KeyboardInterrupt:
        print(value)
        print("Program terminated manually!")
        os._exit(1)


current_position()
# Point(x=1828, y=982). color: (237, 237, 237)
