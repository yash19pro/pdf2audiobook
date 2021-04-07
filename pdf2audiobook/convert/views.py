from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def book_upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        file_save = FileSystemStorage()
        file_save.save(uploaded_file.name, uploaded_file)
    return render(request, 'book_upload.html')
