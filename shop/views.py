from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max, Count, Q
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import *
from .serializers import *
from .models import *
from .forms import *
import random


# this method is to find a random record from a given model of models.py
def get_random_object(minimum, model):
    max_id = model.objects.filter(is_deleted=False).aggregate(max_id=Max("id"))['max_id']
    random_id = random.randint(minimum, max_id)
    random_object = model.objects.filter(pk=random_id, is_deleted=False).first()
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
            result = Book.objects.filter(title__contains=title, is_deleted=False)
            all_genre = Genre.objects.filter(is_deleted=False)
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
    genres = Genre.objects.filter(is_deleted=False)
    books = Book.objects.filter(is_deleted=False)[:3]
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
    authors = Author.objects.filter(is_deleted=False)
    genres = Genre.objects.filter(is_deleted=False)
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
    author = Author.objects.filter(is_deleted=False, pk=id)
    genres = Genre.objects.filter(is_deleted=False)
    form = simple_search(request)
    return render(request, 'shop/author-details.html', {'author': author,
                                                        'all_genres': genres,
                                                        'form': form})


def publishers_list(request):
    all_genres = Genre.objects.filter(is_deleted=False)
    point_of_day = get_random_object(1, Author)
    nominated_author = get_random_object(1, Author)
    all_publishers = Publisher.objects.filter(is_deleted=False)
    form = simple_search(request)
    return render(request, 'shop/publishers.html', {'all_genres': all_genres,
                                                    'point_of_day': point_of_day,
                                                    'nominated_author': nominated_author,
                                                    'all_publishers': all_publishers,
                                                    'form': form,
                                                    })


def show_publisher(request, id):
    publisher = Publisher.objects.filter(is_deleted=False, pk=id)
    all_genres = Genre.objects.filter(is_deleted=False)
    form = simple_search(request)
    return render(request, 'shop/publisher-details.html', {'publisher': publisher,
                                                           'all_genres': all_genres,
                                                           'form': form,
                                                           })


def book_by_genre(request, id):
    genre = Genre.objects.filter(is_deleted=False, pk=id)
    all_genres = Genre.objects.filter(is_deleted=False)
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
    book = Book.objects.filter(is_deleted=False, pk=id)
    genres = Genre.objects.filter(is_deleted=False)
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
            result = Book.objects.filter(query_1, is_deleted=False)
            genres = Genre.objects.filter(is_deleted=False)
            form = simple_search(request)
            return render(request, 'shop/advanced_search.html', {'result': result,
                                                                 'form': form,
                                                                 'all_genres': genres})
    else:
        adv_form = AdvancedSearch()
        genres = Genre.objects.filter(is_deleted=False)
        form = simple_search(request)
        return render(request, 'shop/advanced_search_form.html', {'adv_form': adv_form,
                                                                  'all_genres': genres,
                                                                  'form': form})


def about_us(request):
    genres = Genre.objects.filter(is_deleted=False)
    form = simple_search(request)
    return render(request, 'aboutus.html', {'all_genres': genres,
                                            'form': form})


def contact_us(request):
    genres = Genre.objects.filter(is_deleted=False)
    form = simple_search(request)
    return render(request, 'contactus.html', {'all_genres': genres,
                                              'form': form})


# REST API methods using DRF
@api_view(['GET', 'POST'])
def api_book_list(request):
    if request.method == 'GET':
        book_list = Book.objects.filter(is_deleted=False)
        serializer = BookSerializer(book_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def api_book_details(request, pk, format=None):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.is_deleted = False
        return Response(status=status.HTTP_204_NO_CONTENT)
