from django.shortcuts import render

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def contact_us(request):
    return render(request, 'contact_us.html')
