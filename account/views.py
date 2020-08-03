from django.shortcuts import render
from .forms import SignupFrom
from shop import models, views


def signup(request):
    genres = models.Genre.objects.filter(is_deleted=False)
    books = models.Book.objects.filter(is_deleted=False)[:3]
    author = views.get_random_object(1, models.Author)
    nominated_author = views.get_random_object(1, models.Author)
    form = views.simple_search(request)
    context = {'all_genres': genres,
               'nominated_books': books,
               'point_of_day': author,
               'nominated_author': nominated_author,
               'form': form}
    if request.POST:
        signup_form = SignupFrom(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            return render(request, 'home_page.html', context)
        else:
            context['signup_form'] = signup_form
            return render(request, 'account/signup.html', context)
    else:
        signup_form = SignupFrom()
        context['signup_form'] = signup_form
        return render(request, 'account/signup.html', context)
