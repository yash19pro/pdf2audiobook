from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import BooksForm
from .models import Books

import os


# Create your views here.
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
            return redirect('book-list')
    return render(request, 'book_upload.html', {'form': form})


def book_delete(request, pk):
    if request.method == 'POST':
        book = Books.objects.get(pk = pk)
        book.delete()
    return redirect('book-list')


def book_list(request):
    books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})
