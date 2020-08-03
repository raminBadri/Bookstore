from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render
from .tokens import account_activation_token
from shop import models, views
from .forms import SignupFrom
from .models import ShopUser


def requirements_filler(request):
    genres = models.Genre.objects.filter(is_deleted=False)
    books = models.Book.objects.filter(is_deleted=False)[:3]
    author = views.get_random_object(1, models.Author)
    nominated_author = views.get_random_object(1, models.Author)
    form = views.simple_search(request)
    result = {'all_genres': genres,
              'nominated_books': books,
              'point_of_day': author,
              'nominated_author': nominated_author,
              'form': form}
    return result


def signup(request):
    context = requirements_filler(request)
    if request.POST:
        signup_form = SignupFrom(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Account Verification'
            email_context = render_to_string('account/active.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'domain': current_site.domain,
                'token': account_activation_token.make_token(user),
            })
            email_addr = signup_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, email_context, to=[email_addr])
            email.send()
            msg = 'باتشکر، لینک فعال سازی به ایمیل شما ارسال شد.' \
                  ' جهت فعال سازی حساب کاربری خود بروی آن کلیک نمایید'
            messages.add_message(request, messages.SUCCESS, msg)
            return render(request, 'home_page.html', context)
        else:
            context['signup_form'] = signup_form
            return render(request, 'account/signup.html', context)
    else:
        signup_form = SignupFrom()
        context['signup_form'] = signup_form
        return render(request, 'account/signup.html', context)


def activate(request, uidb64, token):
    context = requirements_filler(request)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = ShopUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ShopUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token) and not user.is_active:
        user.is_active = True
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'فعال سازی با موفقیت انجام شد')
        return render(request, 'home_page.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'فعال سازی با مشکل مواجه شد. لطفا دوباره تلاش کنید')
        return render(request, 'home_page.html', context)
