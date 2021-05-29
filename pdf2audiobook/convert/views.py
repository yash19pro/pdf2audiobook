from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import BooksForm, EditorialForm
from .models import Books, Editorial
import os

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

            # Grab the index
            index = request.POST['index']

            # Convert the given index to text and store the audio files

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
