import img2pdf
import os
from time import sleep
import sys


def convert_e_book_to_pdf():
    listFileNamesLen = len(os.listdir('screen_shots'))
    pdfFile = open("out.pdf", "wb")

    with open("out.pdf", "wb") as f:
        f.write(img2pdf.convert(
            [os.path.join(sys.path[0], "../screen_shots/screen-{}.jpg".format(i)) for i in range(listFileNamesLen)]))