# importing the necessary libraries
from pdf2image import convert_from_path
import os
import re
from stat import S_IREAD

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
            os.makedirs('{}/pdf2audiobook/media/audiobook_books/{}/images/{}'.format(self.pdfpath, self.pdfname, self.chapter_name), exist_ok=True)
        except FileExistsError:
            pass

        for i in range(self.start, self.end + 1):
            self.pages[i].save('{}/pdf2audiobook/media/audiobook_books/{}/images/{}/page{}.jpg'.format(self.pdfpath, self.pdfname,
                                                                                self.chapter_name, i - self.start), 'JPEG')
            print('Page ' + str(i - self.start) + " done...")

def makemyindex():
    index = dict()
    index_string = input("Enter the index string in following format:\n"
                         "No. of chapters : page ranges separated by commas (E.g. 3 : 1-4, 5-10, 11-15)\n"
                         "Index string: ").rstrip()
    index_string = re.split(r':', index_string)
    n = int(index_string[0])
    page_ranges = re.split(r',', index_string[1])
    if len(page_ranges) != n:
        print("Page ranges does not match with number of chapters.")
        return index
    counter = 0
    for i in page_ranges:
        chapter_bounds_split = re.split(r"-", i)
        index["Chapter {}".format(counter)] = (int(chapter_bounds_split[0]), int(chapter_bounds_split[1]))
        counter += 1
    print(index)
    return index


def pager(pdfpath, pdfname):
    # Convert PDF pages to images
    pages = convert_from_path(poppler_path="C:\\poppler-21.02.0\\Library\\bin",
                              pdf_path="{}/pdf2audiobook/media/books/{}.pdf".format(pdfpath, pdfname),
                              dpi=300, fmt="jpeg", grayscale=True, size=(2921, 3449))
    os.makedirs('{}/pdf2audiobook/media/audiobook_books/{}'.format(pdfpath, pdfname), exist_ok=True)
    return pages


name_of_pdf = input("Name of the book: ").strip()

Index = makemyindex()
index_keys = list(Index.keys())
index_values = list(Index.values())

pdf_pages = pager(os.path.dirname(__file__), name_of_pdf)
for x in range(len(Index)):
    a = Pdf2images(name_of_pdf, index_keys[x], int(index_values[x][0]), int(index_values[x][1]), pdf_pages)
    a.converter()
f = open('{}/pdf2audiobook/media/audiobook_books/{}/Index.txt'.format(os.path.dirname(__file__), name_of_pdf), 'w')
f.write(str(Index))
f.close()

os.chmod('{}/pdf2audiobook/media/audiobook_books/{}/Index.txt'.format(os.path.dirname(__file__), name_of_pdf), S_IREAD)
