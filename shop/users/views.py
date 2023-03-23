import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

import users.models
import users.services
from users.forms import CustomUserChangeForm, ProfileChangeForm, SignUpForm


def signup(request: HttpRequest) -> HttpResponse:
    """регистрация пользователя"""
    form = SignUpForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        user = form.save(commit=False)
        user.is_active = settings.USER_IS_ACTIVE
        user.save()
        profile = users.models.Profile(user=user)
        profile.save()
        if not settings.USER_IS_ACTIVE:
            users.services.activation_email(
                request, 'users:activate_user', user
            )
            messages.success(
                request,
                f'На вашу почту {user.email} было '
                'отправлено письмо с активацией'
            )
        else:
            messages.success(request, 'Спасибо за регистрацию!')
            login(request, user)
        return redirect('homepage:homepage')
    return render(request, 'users/signup.html', {'form': form})


def activate_user(
    request: HttpRequest, uidb64: str, token: str
) -> HttpResponse:
    """активация аккаунта пользователя"""
    try:
        user = users.models.ShopUser.objects.get(
            pk=force_str(urlsafe_base64_decode(uidb64))
        )
    except Exception:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, 'Спасибо за активацию аккаунта'
        )
    else:
        messages.error(
            request,
            'Ссылка активации неверна.'
        )
    return redirect('homepage:homepage')


def reset_login_attempts(
    request: HttpRequest, uidb64: str, token: str
) -> HttpResponse:
    """активация аккаунта после превышения попыток"""
    try:
        user = users.models.ShopUser.objects.get(
            pk=force_str(urlsafe_base64_decode(uidb64))
        )
    except Exception:
        user = None
    if (
        user and default_token_generator.check_token(user, token)
        and (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()
        > user.datetime_blocked.timestamp()
    ):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Спасибо за активацию аккаунта, теперь вы можете войти'
        )
    else:
        messages.error(
            request,
            'Ссылка активации неверна.'
        )
    return redirect('homepage:homepage')


@staff_member_required
def user_list(request: HttpRequest) -> HttpResponse:
    """список пользователей"""
    context = {
        'users': users.models.ShopUser.objects.get_only_useful_list_fields()
    }
    return render(
        request, 'users/user_list.html', context=context
    )


@staff_member_required
def user_detail(request: HttpRequest, user_id: int) -> HttpResponse:
    """один пользователь"""
    context = {
        'user': get_object_or_404(
            users.models.ShopUser.objects.get_only_useful_detail_fields(),
            pk=user_id
        )
    }
    return render(
        request, 'users/user_detail.html', context=context
    )


@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    """профиль пользователя"""
    user_form = CustomUserChangeForm(instance=request.user)
    profile_form = ProfileChangeForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileChangeForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно изменен!')
    context = {
        'user': get_object_or_404(
            users.models.ShopUser.objects.get_only_useful_detail_fields(),
            pk=request.user.pk
        ),
        'forms': [user_form, profile_form]
    }
    return render(
        request, 'users/profile.html', context=context
    )