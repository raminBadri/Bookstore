from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    genres = Genre.objects.all()
    books = Book.objects.all()[:3]
    return render(request, 'home_page.html', {'all_genres': genres,
                                              'nominated_books': books
                                              })
