"""pdf2audiobook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from convert.views import about_us, book_delete, book_list, book_upload, contact_us, how_to_use, landing_page, first_page, chapter_page
from player.views import audio_player

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name = 'landing-page'),
    path('contact_us/', contact_us, name = 'contact-us-page'),
    path('book/', book_list, name = 'book-list'),
    path('book-upload/', book_upload, name = 'book-upload'),
    path('book/<int:pk>/', book_delete, name = 'book-delete'),
    path('book/<slug:name>/', first_page, name = 'chapterList'),
    path('book/<slug:name>/<int:chapID>', chapter_page, name = 'chapter'),
    path('about_us/', about_us, name = 'about-us-page'),
    path('how_to_use/', how_to_use, name = 'how-to-use-page'),
    path('audio/', audio_player, name = 'audiobook-player'),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
