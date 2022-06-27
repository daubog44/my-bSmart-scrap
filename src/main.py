from srpit import main, move_b_smart, move_to_code, close_popup, click_e_book, click_maximaze, click_mode_single_page, get_screenshot, click_next_page
import pyautogui
from PDFMaker import convert_e_book_to_pdf
from time import sleep


def get_pages_from_file():
    lines = 0
    with open("out.txt", "r") as f:
        lines = f.readlines()
    return lines[0]


def bot_screenshots_reapet():
    pages = get_pages_from_file()
    for i in range(0, int(pages-1)):
        if i == 0:
            print(i)
            get_screenshot(i)
        else:
            get_screenshot(i, False, False)
        click_next_page()
        sleep(1.5)


def start_bot():
    print("BEFORE STARTING BOT you should have taken the screenshot of the cover of the e-book you want to select and placed it in the find-buttons folder")
    main()
    move_b_smart()
    close_popup()
    click_e_book()
    click_mode_single_page()
    bot_screenshots_reapet()
    convert_e_book_to_pdf()


start_bot()
