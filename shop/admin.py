from django.contrib import admin
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Here I'm using some customization options for django admin panel:


    list_display      =>    what should be shown in Book admin page
    filter_horizontal =>    changes add/change for genre interface
    list_filter       =>    right filter panel keys
    search_fields     =>    search box basis keys
    raw_id_fields     =>    changes 1=>N, N=>M fields display form in add/change actions
    """

    list_display = ['title', 'year', 'author', 'price', 'creation_date', 'publisher']
    filter_horizontal = ('genre',)
    list_filter = ('title', 'genre', 'author')
    search_fields = ('title', 'author__name')
    raw_id_fields = ('genre', 'author')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Publisher)
admin.site.register(Score)
admin.site.register(Comment)
admin.site.register(Genre)
