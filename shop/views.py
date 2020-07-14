from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max, Count, Q
from django.views.generic import *
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


# this view fills home page's requirements
def index(request):
    genres = Genre.objects.all()
    books = Book.objects.all()[:3]
    author = get_random_object(1, Author)
    nominated_author = get_random_object(1, Author)
    return render(request, 'home_page.html', {'all_genres': genres,
                                              'nominated_books': books,
                                              'point_of_day': author,
                                              'nominated_author': nominated_author,
                                              })


# we could use class based views too
def list_authors(request):
    authors = Author.objects.all()
    genres = Genre.objects.all()
    author = get_random_object(1, Author)
    nominated_author = get_random_object(1, Author)
    return render(request, 'shop/authors.html', {'all_authors': authors,
                                                 'all_genres': genres,
                                                 'point_of_day': author,
                                                 'nominated_author': nominated_author,
                                                 })


def show_author(request, id):
    author = Author.objects.get(pk=id)
    genres = Genre.objects.all()
    return render(request, 'shop/author-details.html', {'author': author,
                                                        'all_genres': genres})


# class based list and detail view sample for publisher model
class PublisherListView(ListView):
    model = Publisher
    template_name = 'shop/publishers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_genres'] = Genre.objects.all()
        context['point_of_day'] = get_random_object(1, Author)
        context['nominated_author'] = get_random_object(1, Author)
        return context


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'shop/publisher-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_genres'] = Genre.objects.all()
        return context


class BookDetailView(DetailView):
    model = Genre
    template_name = 'shop/book_by_genre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_genres'] = Genre.objects.all()
        context['point_of_day'] = get_random_object(1, Author)
        context['nominated_author'] = get_random_object(1, Author)
        return context
############################


def show_book(request, pk):
    book = Book.objects.get(pk=pk)
    genres = Genre.objects.all()
    return render(request, 'shop/book-details.html', {'book': book,
                                                      'all_genres': genres})


def about_us(request):
    genres = Genre.objects.all()
    return render(request, 'aboutus.html', {'all_genres': genres})


def contact_us(request):
    genres = Genre.objects.all()
    return render(request, 'contactus.html', {'all_genres': genres})


