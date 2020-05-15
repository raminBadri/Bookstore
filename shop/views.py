from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max, Count, Q
import random
from .models import *


# this method is to find a random record from a given model of models.py
def get_random_object(minimum, model):
    max_id = model.objects.all().aggregate(max_id=Max("id"))['max_id']
    random_id = random.randint(minimum, max_id)
    random_object = model.objects.filter(pk=random_id).first()
    return random_object


# this method is to find best 3 books of a given genre to
# fill home page's best books of a genre box
def find_best_books():
    result = Genre.objects.annotate(Count('book'))
    for _ in result:
        if _.book__count >= 3:
            return _


def index(request):
    genres = Genre.objects.all()
    books = Book.objects.all()[:3]
    author = get_random_object(1, Author)
    nominated_author = get_random_object(1, Author)
    nominated_genre = find_best_books()
    return render(request, 'home_page.html', {'all_genres': genres,
                                              'nominated_books': books,
                                              'point_of_day': author,
                                              'nominated_author': nominated_author,
                                              })
