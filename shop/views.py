from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max
import random
from .models import *


def index(request):
    genres = Genre.objects.all()
    books = Book.objects.all()[:3]
    max_id = Author.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        author = Author.objects.filter(pk=pk).first()
        if author.quote:
            break
    pk = random.randint(1, max_id)
    nominated_author = Author.objects.get(pk=pk)
    return render(request, 'home_page.html', {'all_genres': genres,
                                              'nominated_books': books,
                                              'point_of_day': author,
                                              'nominated_author': nominated_author,
                                              })
