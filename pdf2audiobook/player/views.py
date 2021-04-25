from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import Song

def audio_player(request):
    paginator = Paginator(Song.objects.all(), 1)
    page_number = request.GET.get('page')
    print(page_number)
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context={
		"page_obj": page_obj
	}
    return render(request, "player.html", context)