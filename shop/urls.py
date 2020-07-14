from django.views.generic import RedirectView
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='home_page'),
    path('all-authors/', views.list_authors, name='all_authors'),
    path('author-details/<int:id>', views.show_author, name='author_details'),
    path('wikipedia/<str:name>/',
         RedirectView.as_view(url="https://fa.wikipedia.org/wiki/%(name)s"), name='wiki'),
    path('all-publishers/', views.PublisherListView.as_view(), name='all_publishers'),
    path('publisher-detail/<int:pk>', views.PublisherDetailView.as_view(), name='publisher_details'),
    path('book-details/<int:pk>', views.show_book, name='book_details'),
    path('aboutus/', views.about_us, name='aboutus'),
    path('contactus/', views.contact_us, name='contactus'),
    path('genres/<int:pk>', views.BookDetailView.as_view(), name='book_by_genre'),

]
