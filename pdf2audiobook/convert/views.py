from django.shortcuts import render

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def book_upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request, 'book_upload.html')
