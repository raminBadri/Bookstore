from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max, Count, Q
from django.views.generic import *
import random
from .models import *
from .forms import *


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


# simple book search method
def simple_search(request):
    if request.method == "POST":
        form = SimpleSearch(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            result = Book.objects.filter(title__contains=title)
            all_genre = Genre.objects.all()
            if result.count() != 0:
                return render(request, 'shop/simple_search.html', {'result': result,
                                                                   'all_genres': all_genre,
                                                                   'form': form})
            else:
                return render(request, 'shop/simple_search.html', {'all_genres': all_genre,
                                                                   'form': form})
    else:
        form = SimpleSearch()
        return form


# this view fills home page's requirements
def index(request):
    genres = Genre.objects.all()
    books = Book.objects.all()[:3]
    author = get_random_object(1, Author)
    nominated_author = get_random_object(1, Author)
    form = simple_search(request)
    return render(request, 'home_page.html', {'all_genres': genres,
                                              'nominated_books': books,
                                              'point_of_day': author,
                                              'nominated_author': nominated_author,
                                              'form': form,
                                              })


# we could use class based views too
def authors_list(request):
    authors = Author.objects.all()
    genres = Genre.objects.all()
    author = get_random_object(1, Author)
    nominated_author = get_random_object(1, Author)
    form = simple_search(request)
    return render(request, 'shop/authors.html', {'all_authors': authors,
                                                 'all_genres': genres,
                                                 'point_of_day': author,
                                                 'nominated_author': nominated_author,
                                                 'form': form,
                                                 })


def show_author(request, id):
    author = Author.objects.get(pk=id)
    genres = Genre.objects.all()
    form = simple_search(request)
    return render(request, 'shop/author-details.html', {'author': author,
                                                        'all_genres': genres,
                                                        'form': form})


def publishers_list(request):
    all_genres = Genre.objects.all()
    point_of_day = get_random_object(1, Author)
    nominated_author = get_random_object(1, Author)
    all_publishers = Publisher.objects.all()
    form = simple_search(request)
    return render(request, 'shop/publishers.html', {'all_genres': all_genres,
                                                    'point_of_day': point_of_day,
                                                    'nominated_author': nominated_author,
                                                    'all_publishers': all_publishers,
                                                    'form': form,
                                                    })


def show_publisher(request, id):
    publisher = Publisher.objects.get(pk=id)
    all_genres = Genre.objects.all()
    form = simple_search(request)
    return render(request, 'shop/publisher-details.html', {'publisher': publisher,
                                                           'all_genres': all_genres,
                                                           'form': form,
                                                           })


def book_by_genre(request, id):
    genre = Genre.objects.get(pk=id)
    all_genres = Genre.objects.all()
    point_of_day = get_random_object(1, Author)
    nominated_author = get_random_object(1, Author)
    form = simple_search(request)
    return render(request, 'shop/book_by_genre.html', {'genre': genre,
                                                       'all_genres': all_genres,
                                                       'point_of_day': point_of_day,
                                                       'nominated_author': nominated_author,
                                                       'form': form
                                                       })


def show_book(request, pk):
    book = Book.objects.get(pk=pk)
    genres = Genre.objects.all()
    form = simple_search(request)
    return render(request, 'shop/book-details.html', {'book': book,
                                                      'all_genres': genres,
                                                      'form': form})


#############################
# class based list and detail view sample for publisher model
# class PublisherListView(ListView):
#     model = Publisher
#     template_name = 'shop/publishers.html'
#
#     def get(self, request, **kwargs):
#         return simple_search(request)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['all_genres'] = Genre.objects.all()
#         context['point_of_day'] = get_random_object(1, Author)
#         context['nominated_author'] = get_random_object(1, Author)
#         return context
#
#
# class PublisherDetailView(DetailView):
#     model = Publisher
#     template_name = 'shop/publisher-details.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['all_genres'] = Genre.objects.all()
#         return context
#
#
# class BookDetailView(DetailView):
#     model = Genre
#     template_name = 'shop/book_by_genre.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['all_genres'] = Genre.objects.all()
#         context['point_of_day'] = get_random_object(1, Author)
#         context['nominated_author'] = get_random_object(1, Author)
#         return context
############################


def advanced_search(request):
    if request.method == 'POST':
        form = AdvancedSearch(request.POST)
        if form.is_valid():
            query_1 = Q(author__name__contains=form.cleaned_data['author_name']) &\
                      Q(title__contains=form.cleaned_data['book_title']) &\
                      Q(publisher__title__contains=form.cleaned_data['publisher_title']) &\
                      Q(genre__title__contains=form.cleaned_data['genre_title'])
            # query_2 = Q(title__contains=form.cleaned_data['book_title']) \
            #           | Q(author__name__contains=form.cleaned_data['author_name']) \
            #           | Q(publisher__title__contains=form.cleaned_data['publisher_title']) \
            #           | Q(genre__title__contains=form.cleaned_data['genre_title'])
            result = Book.objects.filter(query_1)
            genres = Genre.objects.all()
            form = simple_search(request)
            return render(request, 'shop/advanced_search.html', {'result': result,
                                                                 'form': form,
                                                                 'all_genres': genres})
    else:
        adv_form = AdvancedSearch()
        genres = Genre.objects.all()
        form = simple_search(request)
        return render(request, 'shop/advanced_search_form.html', {'adv_form': adv_form,
                                                                  'all_genres': genres,
                                                                  'form': form})


def about_us(request):
    genres = Genre.objects.all()
    form = simple_search(request)
    return render(request, 'aboutus.html', {'all_genres': genres,
                                            'form': form})


def contact_us(request):
    genres = Genre.objects.all()
    form = simple_search(request)
    return render(request, 'contactus.html', {'all_genres': genres,
                                              'form': form})
