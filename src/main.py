from srpit import move_b_smart, move_to_code, click_e_book, click_maximaze, click_mode_single_page, get_screenshot, click_next_page
import pyautogui
from PDFMaker import convert_e_book_to_pdf
from time import sleep
import traceback
import os

def bot_screenshots_reapet():
    for i in range(0, 10000):
        try:
            if i == 0:
                get_screenshot(i, first=True)
            else:
                possible_err = get_screenshot(i)
                if possible_err == True:
                    print("Error in get_screenshot")
                    continue
            click_next_page()
            sleep(1.5)
        except Exception as e:
            print("FINISH COLLECT PAGES")
            print(e)
            break


def start_bot():
    e_book = [file.split(".")[0] for file in os.listdir(
        os.path.join(os.getcwd(), "find_buttons"))]
    if not "e-book" in e_book:
        print("bot scraping for e-books on my-bsmart platform. To boot, install the requirements, open my-bsmart and take a screenshot of the e-book cover and put it in find_buttons folder as e-book.png then start the bot of main script. The output is the pdf of the e-book")
        return
    move_b_smart()
    click_e_book()
    click_mode_single_page()
    bot_screenshots_reapet()
    convert_e_book_to_pdf()


start_bot()
