from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.auth.tokens import default_token_generator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

import users.models
import users.services
from users.forms import (
    CustomUserChangeForm,
    ProfileChangeForm,
    SignUpForm,
)
from users.tokens import token_7_days


class SignupView(FormView):
    """регистрация пользователя"""
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get_success_url(self) -> str:
        """получаем адрес для редиректа в случае валидной формы"""
        return reverse('homepage:homepage',)

    def form_valid(self, form: SignUpForm) -> HttpResponsePermanentRedirect:
        """при валидной форме создается новый пользователь
        и активируется(сразу или письмо для активации приходит на почту)"""
        user = form.save(commit=False)
        user.is_active = settings.USER_IS_ACTIVE
        user.save()
        profile = users.models.Profile(user=user)
        profile.save()
        if not settings.USER_IS_ACTIVE:
            users.services.activation_email(
                self.request, 'users:activate_user', user
            )
            messages.success(
                self.request,
                f'На вашу почту {user.email} было '
                'отправлено письмо с активацией',
            )
        else:
            messages.success(self.request, 'Спасибо за регистрацию!')
            login(self.request, user)
        return super().form_valid(form)


class ActivateUserView(View):
    """Активирует аккаунт пользователя"""
    def get(
        self, request: HttpRequest, uidb64: str, token: str
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
            messages.success(request, 'Спасибо за активацию аккаунта')
        else:
            messages.error(request, 'Ссылка активации неверна.')
        return redirect('homepage:homepage')


class ResetLoginAttempts(View):
    def get(self, request: HttpRequest, uidb64: str, token: str
            ) -> HttpResponsePermanentRedirect:
        """активация аккаунта после превышения попыток"""
        try:
            user = users.models.ShopUser.objects.get(
                pk=force_str(urlsafe_base64_decode(uidb64))
            )
        except Exception:
            user = None
        if user and token_7_days.check_token(user, token):
            user.is_active = True
            messages.success(
                request, 'Спасибо за активацию аккаунта,'
                'теперь вы можете войти'
            )
            user.login_attempts = settings.LOGIN_ATTEMPTS - 1
            user.save()
        else:
            messages.error(request, 'Ссылка активации неверна.')
        return redirect('homepage:homepage')


class UserListView(PermissionRequiredMixin, ListView):
    """список пользователей"""
    permission_required = 'is_staff'
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    queryset = users.models.ShopUser.objects.get_only_useful_list_fields()


class UserDetailView(PermissionRequiredMixin, DetailView):
    """детальная информация о пользователе"""
    permission_required = 'is_staff'
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
    queryset = users.models.ShopUser.objects.get_only_useful_detail_fields()


class UserProfileView(LoginRequiredMixin, View):
    """Профиль пользоватея"""
    template_name = 'users/signup.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileChangeForm(instance=request.user.profile)
        context = {
            'user': get_object_or_404(
                users.models.ShopUser.objects.get_only_useful_detail_fields(),
                pk=request.user.pk,
            ),
            'forms': [user_form, profile_form],
        }
        return render(request, 'users/profile.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponsePermanentRedirect:
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileChangeForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно изменен!')
        return redirect('users:user_profile')
