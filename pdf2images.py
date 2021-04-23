# importing the necessary libraries
from pdf2image import convert_from_path
import os
import re


class Pdf2images:
    # Constructor
    def __init__(self, pdfname, chapter_name, start, end, pages):
        self.pdfname = pdfname
        self.start = start
        self.end = end
        self.pdfpath = os.path.dirname(__file__)
        self.chapter_name = chapter_name
        self.pages = pages

    def converter(self):
        # Creates a folder to store images
        try:
            os.mkdir('{}/pdf2audiobook/media/{}/{}'.format(self.pdfpath, self.pdfname, self.chapter_name))
        except FileExistsError:
            pass

        for i in range(self.start, self.end + 1):
            self.pages[i].save('{}/pdf2audiobook/media/{}/{}/page{}.jpg'.format(self.pdfpath, self.pdfname,
                                                                                self.chapter_name, i - self.start), 'JPEG')
            print('Page ' + str(i - self.start) + " done...")


class Makemyindex:
    def makemyindex(self):
        index = dict()
        n = int(input("No of chapters in the book: "))
        print("Enter starting and ending page number from pdf separated by '-'")
        for i in range(1, n+1):
            chapter_bounds = input("Chapter {}: ".format(i)).strip()
            chapter_bounds_split = re.split(r"-", chapter_bounds)
            index["Chapter {}".format(i)] = (int(chapter_bounds_split[0]), int(chapter_bounds_split[1]))
        return index


class Pager:
    def pager(self, pdfpath, pdfname):
        # Convert PDF pages to images
        pages = convert_from_path(poppler_path="C:\\poppler-21.02.0\\Library\\bin",
                                  pdf_path="{}/pdf2audiobook/media/books/{}.pdf".format(pdfpath, pdfname),
                                  dpi=300, fmt="jpeg", grayscale=True, size=(2921, 3449))
        os.mkdir('{}/pdf2audiobook/media/{}'.format(pdfpath, pdfname))
        return pages


name_of_pdf = input("Name of the book: ").strip()

M = Makemyindex()
Index = M.makemyindex()
index_keys = list(Index.keys())
index_values = list(Index.values())

P = Pager()
pdf_pages = P.pager(os.path.dirname(__file__), name_of_pdf)
for x in range(len(Index)):
    a = Pdf2images(name_of_pdf, index_keys[x], index_values[x][0], index_values[x][1], pdf_pages)
    a.converter()
