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

def book_upload(request):
    form = BooksForm()
    if request.method == 'POST':
        form = BooksForm(request.POST, request.FILES)
        # diro = os.getcwd() + '/media/books/'
        # title = str(request.FILES['file'])
        # final_title = ""
        # for x in title:
        #     if x == ' ':
        #         final_title  += '_'
        #     else:
        #         final_title += x
        # request.FILES['file'].name = final_title
        # print(request.FILES['file'].name)
        # print(request.FILES)
        if form.is_valid():
            form.save()
            # os.rename(diro + final_title, diro + request.POST['title'] + '.pdf')
            return redirect('book-list')
    return render(request, 'book_upload.html', {'form': form})

def book_delete(request, pk):
    if request.method == 'POST':
        book = Books.objects.get(pk = pk)
        book.delete()
    return redirect('landing-page')

def book_list(request):
    books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})
