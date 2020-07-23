from django.views.generic import RedirectView
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='home_page'),
    path('all-authors/', views.authors_list, name='all_authors'),
    path('author-details/<int:id>', views.show_author, name='author_details'),
    path('wikipedia/<str:name>/',
         RedirectView.as_view(url="https://fa.wikipedia.org/wiki/%(name)s"), name='wiki'),
    path('all-publishers/', views.publishers_list, name='all_publishers'),
    path('publisher-details/<int:id>', views.show_publisher, name='publisher_details'),
    path('book-details/<int:pk>', views.show_book, name='book_details'),
    path('book-by-genre/<int:id>', views.book_by_genre, name='book_by_genre'),
    path('search/', views.simple_search, name='simple_search'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    path('advanced-search-result/', views.advanced_search, name='advanced_search_result'),
    path('aboutus/', views.about_us, name='aboutus'),
    path('contactus/', views.contact_us, name='contactus'),
    # api urls
    path('api/books', views.api_book_list, name='api-book-list'),
    path('api/book-details/<int:pk>/', views.api_book_details, name='api-book-details'),
    path('api/authors', views.api_author_list, name='api-author-list'),
    path('api/author-details/<int:pk>/', views.api_author_list, name='api-author-details'),
    path('api/publisher-list', views.api_publisher_list, name='api-publisher-list'),
    # class based view urls
    # path('all-publishers/', views.PublisherListView.as_view(), name='all_publishers'),
    # path('publisher-detail/<int:pk>', views.PublisherDetailView.as_view(), name='publisher_details'),
    # path('genres/<int:pk>', views.BookDetailView.as_view(), name='book_by_genre'),

]
