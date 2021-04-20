# importing the necessary libraries
from pdf2image import convert_from_path
import os


class Pdf2images:
    # Constructor
    def __init__(self, pdfname, start, end):
        self.pdfname = pdfname
        self.start = start
        self.end = end
        self.pdfpath = os.path.dirname(__file__)

    def converter(self):
        # Creates a folder to store images
        os.mkdir('{}/pdf2audiobook/media/{}'.format(self.pdfpath, self.pdfname))

        # Convert PDF pages to images
        pages = convert_from_path(poppler_path="C:\\poppler-21.02.0\\Library\\bin", pdf_path="{}/pdf2audiobook/media/{}.pdf".format(self.pdfpath, self.pdfname), dpi=300, fmt="jpeg", grayscale=True, size=(2921, 3449))
        for i in range(self.start, self.end + 1):
            pages[i].save('{}/pdf2audiobook/media/{}/page{}.jpg'.format(self.pdfpath, self.pdfname, i - self.start), 'JPEG')
            print('Page ' + str(i - self.start) + " done...")

a = Pdf2images("IAG", 15, 17)
a.converter()