import img2pdf
import os
from time import sleep

def convert_e_book_to_pdf():
    listFileNamesLen = len(os.listdir('screen_shots'))
    pdfFile = open("out.pdf", "wb")
    print(listFileNamesLen)

    with open("out.pdf", "wb") as f:
        f.write(img2pdf.convert(
            [r"./screen_shots/screen-{}.jpeg".format(i) for i in range  (listFileNamesLen)]))