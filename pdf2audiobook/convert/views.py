from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import BooksForm
from .models import Books

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def book_upload(request):
    form = BooksForm()
    if request.method == 'POST':
        form = BooksForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    return render(request, 'book_upload.html', {'form': form})

def book_list(request):
    books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})
