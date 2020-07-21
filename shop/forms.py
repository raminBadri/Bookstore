from django import forms


class SimpleSearch(forms.Form):
    title = forms.CharField(label="", max_length=255)


class AdvancedSearch(forms.Form):
    book_title = forms.CharField(label='عنوان کتاب', max_length=255)
    author_name = forms.CharField(label='نام نویسنده', max_length=255)
    publisher_title = forms.CharField(label='نام انتشارات', max_length=255)
    genre_title = forms.CharField(label='ژانر کتاب', max_length=255)
