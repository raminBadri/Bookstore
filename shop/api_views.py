"""
Here we have all our API views,
 In order to show you two of the best ways of implementing API in DRF i'm using:
    1) Function based API for Authors
    2) Class based API which are:
        a. ViewSets API for Publishers
        b. ModelViewSets for Books
But regardless of them, I write an example of function based API views for Book object, too.
"""

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from account.models import ShopUser
from .serializers import *
from .models import *


"""
This is a function based API as mentioned above, but 
it's not a useful way so I only write it as comment.

@api_view(['GET', 'POST'])  # This decorator is used to block any other requests except GET and POST
@permission_classes([IsAuthenticated])  # This decorator allows for authenticated users only to pass
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
"""
###########################
"""
In real projects, we use ViewSets and ModelViewSets to create standard API with DRF
"""


class BookViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for handling GET, POST, PUT and DELETE client requests for book model.
    GET => list, retrieve
    POST => create
    PUT => update
    DELETE => destroy
    """

    def list(self, request):
        queryset = Book.objects.filter(is_deleted=False)
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Book.objects.filter(is_deleted=False)
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def update(self, request, pk=None):
        queryset = Book.objects.filter(is_deleted=False)
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(book)

    def destroy(self, request, pk=None):
        queryset = Book.objects.filter(is_deleted=False)
        book = get_object_or_404(queryset, pk=pk)
        book.is_deleted = True
        book.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A simple ModelViewSet for authors.
    THIS ONE IS AWESOME!
    """
    queryset = Author.objects.filter(is_deleted=False)
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    """
    A simple ModelViewSet for publishers.
    THIS ONE IS AWESOME!
    """
    queryset = Publisher.objects.filter(is_deleted=False)
    serializer_class = PublisherSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = ShopUser.objects.filter(is_active=True)
    serializer_class = UserSerializer
