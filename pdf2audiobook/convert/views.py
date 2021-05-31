# Django libraries
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.static import serve
from django.http import HttpResponse
from .forms import BooksForm
from .models import Books

# Other libraries
import os
from pdf2images import Pdf2images
from images2audio import Image2audio
from pdf2image import convert_from_path
from editorial2audio import Editorial2audiobook
import re
import mimetypes
from directory_downloader import DDownloader
import asyncio

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

			if index_string == 'editorial':
				print('in editorial')
				a = Editorial2audiobook(2, None, request.POST['title'])
			else:
				print('in pager')
				pager(name_of_pdf, index_string=index_string)

			return redirect('book-list')
	return render(request, 'book_upload.html', {'form': form})


# async def foo(name):
	# file_path = pathx = os.path.abspath(str(os.path.dirname(__file__)) + '/../media/audiobook_books/' + str(name) + '/audio')
	# url = '127.0.0.1:8000/book/' + str(name) + '/audio'
	# downloader = DDownloader(url, directory="/Users/yashpatel/Downloads")
	# await downloader.download_files()

def download(request, name):
	file_path = pathx = os.path.abspath(str(os.path.dirname(__file__)) + '/../media/audiobook_books/' + str(name) + '/audio')



	# url = '127.0.0.1:8000/book/' + str(name) + '/audio'
	# downloader = DDownloader(url, directory="/Users/yashpatel/Downloads")
	# await downloader.download_files()
	# asyncio.run(foo(name))
	# with open(file_path, 'rb') as pr:
	# 	mime_type, _ = mimetypes.guess_type(file_path)
	# 	res = HttpResponse(pr.read(), content_type=mime_type)
	# 	res['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
	# 	print(mime_type)
	# 	print(res)
	# 	return res


def first_page(request, name):
	# if windows then this
	# pathx = os.path.abspath(str(os.path.dirname(__file__)) + '\\..\\media\\audiobook_books\\' + str(name) + "\\audio")
	# if mac then this
	pathx = os.path.abspath(str(os.path.dirname(__file__)) + '/../media/audiobook_books/' + str(name) + "/audio")
	folders = os.listdir(pathx)
	no_of_folders = [x for x in range(len(folders))]
	context = {'books': no_of_folders, 'bookname': name}
	return render(request, 'chapters.html', context)


def chapter_page(request, name, chapID):
	# if windows then this
	# pathx = os.path.abspath(str(os.path.dirname(__file__)) + '\\..\\media\\audiobook_books\\' + str(name) + "\\audio\\Chapter" + str(chapID))
	# if mac then this
	pathx = os.path.abspath(str(os.path.dirname(
		__file__)) + '/../media/audiobook_books/' + str(name) + "/audio/Chapter" + str(chapID))
	files = os.listdir(pathx)
	no_of_files = [x for x in range(len(files))]
	context = {'books': no_of_files, 'bookname': name, 'chapID': chapID}
	return render(request, 'chap.html', context)


def book_delete(request, pk):
	if request.method == 'POST':
		book = Books.objects.get(pk=pk)
		book.delete()
	return redirect('book-list')


def book_list(request):
	books = Books.objects.all()
	context = {
		'books': books,
	}
	return render(request, 'book_list.html', context)

# a = Editorial2audiobook(
#     2, "https://drive.google.com/file/d/1mbBv1BQaWGr8qp7etr85r6B7imZ6KHLD/view?usp=sharing", request.POST['title'])

# --------------------------
# index: 4 : 4-7, 9-15, 17-19, 21-27
# --------------------------


def pager(pdfname, index_string):
	pdfpath = os.path.dirname(__file__)
	try:
		index = dict()
		index_string = re.split(r':', index_string)
		n = int(index_string[0])
		page_ranges = re.split(r',', index_string[1])
		if len(page_ranges) != n:
			print("Page ranges does not match with number of chapters.")
	except:
		pass
	counter = 0

	pdf_pages = convert_from_path("./media/books/{}.pdf".format(pdfname))
	os.makedirs('./media/audiobook_books/{}'.format(pdfname), exist_ok=True)

	for i in page_ranges:
		chapter_bounds_split = re.split(r"-", i)
		index["Chapter{}".format(counter)] = (
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
