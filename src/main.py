from srpit import move_b_smart, move_to_code, click_e_book, click_maximaze, click_mode_single_page, get_screenshot, click_next_page
import pyautogui
from PDFMaker import convert_e_book_to_pdf
from time import sleep


def get_pages_from_file():
    lines = 0
    with open("out.txt", "r") as f:
        lines = f.readlines()
    return lines[0]


def bot_screenshots_reapet():
    for i in range(0, 10000):
        try:
            if i == 0:
                get_screenshot(i)
            else:
                get_screenshot(i, False, False)
            click_next_page()
            sleep(1.5)
        except Exception as e:
            print(e)
            print("FINISH COLLECT PAGES")
            break


def start_bot():
    print("BEFORE STARTING BOT you should have taken the screenshot of the cover of the e-book you want to select and placed it in the find-buttons folder")
    move_b_smart()
    click_e_book()
    sleep(3)
    click_mode_single_page()
    bot_screenshots_reapet()
    convert_e_book_to_pdf()


start_bot()
