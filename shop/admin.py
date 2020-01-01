from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Score)
admin.site.register(Comment)
admin.site.register(Genre)
