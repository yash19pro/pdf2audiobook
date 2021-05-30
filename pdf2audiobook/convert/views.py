# Django libraries
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import BooksForm, EditorialForm
from .models import Books, Editorial

# Other libraries
import os
from pdf2images import Pdf2images
from images2audio import Image2audio
from pdf2image import convert_from_path
import re
# import pytesseract
# import threading
# import cv2
# import pyttsx3
# import time
# import ast
# from stat import S_IREAD

# Create your views here.

# home page views


def landing_page(request):
    return render(request, 'landing_page.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def about_us(request):
    return render(request, 'about_us.html')


def how_to_use(request):
    return render(request, 'how_to_use.html')


def book_upload(request):
    form = BooksForm()
    if request.method == 'POST':
        request.FILES['file'].name = request.POST['title'] + '.pdf'
        form = BooksForm(request.POST, request.FILES)
        print(type(request.POST))
        print(request.POST)
        if form.is_valid():
            form.save()

            # we have to add the fuction to convert pdf to audio book here, as the form is already saved

            # Covert the pdf to images

            # title of the pdf
            name_of_pdf = request.POST['title'].strip()
            print(name_of_pdf)

            # Grab the index
            index_string = request.POST['index']

            # calling the function
            pager(name_of_pdf, index_string=index_string)

            # Convert the given index to text and store the audio files
            # text = str()

            # def next_img(name):
            # 	global text
            # 	print("Thread execution started")
            # 	time.sleep(5)
            # 	img = cv2.imread(name)
            # 	# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 	# ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
            # 	text = pytesseract.image_to_string(img)
            # 	text = re.sub(r"\b\n", " ", text)
            # 	text = re.sub(r"\n\b", " ", text)
            # 	text = re.sub(r"-\s", "", text)
            # 	print(text)
            # 	print("Thread execution ended")

            # index_keys = list(Index.keys())
            # index_values = list(Index.values())
            # for x in range(len(index_values)):
            # 	a = Image2audio(
            # 		name_of_pdf, index_keys[x], 500, index_values[x][0], index_values[x][1])
            # 	a.converter(text)

            return redirect('book-list')
    return render(request, 'book_upload.html', {'form': form})


def book_delete(request, pk):
    if request.method == 'POST':
        book = Books.objects.get(pk=pk)
        book.delete()
    return redirect('book-list')


def book_list(request):
    books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})


def editorial_upload(request):
    form = EditorialForm()
    if request.method == 'POST':
        request.FILES['file'].name = request.POST['title'] + '.pdf'
        form = EditorialForm(request.POST, request.FILES)
        print(type(request.POST))
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    return render(request, 'editorial_upload.html', {'form': form})

# --------------------------
# index: 4 : 4-7, 9-15, 17-19, 21-27
# --------------------------
# def makemyindex(index_string):
#     index = dict()
#     # index_string = input("Enter the index string in following format:\n"
#     #                      "No. of chapters : page ranges separated by commas (E.g. 3 : 1-4, 5-10, 11-15)\n"
#     #                      "Index string: ").rstrip()
#     index_string = re.split(r':', index_string)
#     n = int(index_string[0])
#     page_ranges = re.split(r',', index_string[1])
#     if len(page_ranges) != n:
#         print("Page ranges does not match with number of chapters.")
#         return index
#     counter = 0
#     for i in page_ranges:
#         chapter_bounds_split = re.split(r"-", i)
#         index["Chapter {}".format(counter)] = (
#             int(chapter_bounds_split[0]), int(chapter_bounds_split[1]))
#         counter += 1
#     print(index)
#     return index

# def pager(pdfpath=os.path.dirname(__file__), pdfname, index):


def pager(pdfname, index_string):
    pdfpath = os.path.dirname(__file__)
    # makemyindex
    index = dict()
    # index_string = input("Enter the index string in following format:\n"
    #                      "No. of chapters : page ranges separated by commas (E.g. 3 : 1-4, 5-10, 11-15)\n"
    #                      "Index string: ").rstrip()
    index_string = re.split(r':', index_string)
    n = int(index_string[0])
    page_ranges = re.split(r',', index_string[1])
    if len(page_ranges) != n:
        print("Page ranges does not match with number of chapters.")
        # return index
    counter = 0

    pdf_pages = convert_from_path("./media/books/{}.pdf".format(pdfname))
    os.makedirs('./media/audiobook_books/{}'.format(pdfname), exist_ok=True)

    for i in page_ranges:
        chapter_bounds_split = re.split(r"-", i)
        index["Chapter {}".format(counter)] = (
            int(chapter_bounds_split[0]), int(chapter_bounds_split[1]))
        counter += 1
    print(index)

    index_keys = list(index.keys())
    index_values = list(index.values())

    for x in range(len(index)):
        a = Pdf2images(pdfname, index_keys[x], int(
            index_values[x][0]), int(index_values[x][1])-1, pdf_pages)
        a.converter()

    for x in range(len(index_values)):
        a = Image2audio(
            pdfname, index_keys[x], 185, index_values[x][0], index_values[x][1])
        a.converter()

    # Convert PDF pages to images

    # Uncomment below lines for Windows
    # pages = convert_from_path(poppler_path="C:\\poppler-21.02.0\\Library\\bin",
    #                           pdf_path="{}/pdf2audiobook/media/books/{}.pdf".format(
    #                               pdfpath, pdfname),
    #                           dpi=300, fmt="jpeg", grayscale=True, size=(2921, 3449))
    # pdf_pages = convert_from_path(
    #     "{}/media/books/{}.pdf".format(pdfpath, pdfname))
    # os.makedirs('{}/media/audiobook_books/{}'.format(pdfpath,
    #                                                  pdfname), exist_ok=True)
    # for x in range(len(index)):
    #     a = Pdf2images(pdfname, index_keys[x], int(
    #         index_values[x][0]), int(index_values[x][1]), pdf_pages)
    #     a.converter()
    # return pages


# name_of_pdf = input("Name of the book: ").strip()


# pdf_pages = pager(os.path.dirname(__file__), name_of_pdf)

# f = open('{}/media/audiobook_books/{}/Index.txt'.format(os.path.dirname(__file__), name_of_pdf), 'w')
# f.write(str(Index))
# f.close()

# os.chmod('{}/media/audiobook_books/{}/Index.txt'.format(os.path.dirname(__file__), name_of_pdf), S_IREAD)

# text = str()

# def next_img(name):
#     global text
#     print("Thread execution started")
#     time.sleep(5)
#     img = cv2.imread(name)
#     # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # ret, img_threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
#     text = pytesseract.image_to_string(img)
#     text = re.sub(r"\b\n", " ", text)
#     text = re.sub(r"\n\b", " ", text)
#     text = re.sub(r"-\s", "", text)
#     print(text)
#     print("Thread execution ended")


# index_keys = list(Index.keys())
# index_values = list(Index.values())
# for x in range(len(index_values)):
#     a = Image2audio(
#         name_of_pdf, index_keys[x], 500, index_values[x][0], index_values[x][1])
#     a.converter(text)
# index: 4 : 4-7, 9-15, 17-19, 21-25
