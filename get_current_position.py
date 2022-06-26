import pyautogui
from time import sleep
import os
def clear(): return os.system('cls')


def current_position():
    while True:
        print(pyautogui.position())
        clear()


current_position()