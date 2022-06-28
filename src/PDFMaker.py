import img2pdf
import os
import glob


def my_func(e):
    return int(e.split('.')[0].split('-')[1])


def convert_e_book_to_pdf():
    listFileNamesLen = len(os.listdir('screen_shots'))

    with open("e-book.pdf", "wb") as f:
        a = glob.glob('screen_shots/*.jpg')
        a.sort(key=my_func)
        f.write(img2pdf.convert(a))
        print("PDF created")
        for f in a:
            os.remove(f)
