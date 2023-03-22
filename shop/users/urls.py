import django.contrib.auth.views
from django.urls import path

import users.forms
import users.views


app_name = 'users'

urlpatterns = [
    path(
        'login/',
        django.contrib.auth.views.LoginView.as_view(
            template_name='users/login.html',
            form_class=users.forms.CustomAuthenticationForm
        ),
        name='login'
    ),
    path(
        'logout/',
        django.contrib.auth.views.LogoutView.as_view(
            template_name='users/logout.html'
        ),
        name='logout'
    ),
    path(
        'password_change/',
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
            form_class=users.forms.CustomPasswordChangeForm
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            form_class=users.forms.CustomPasswordResetForm
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            form_class=users.forms.CustomSetPasswordForm
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('signup/', users.views.signup, name='signup'),
    path(
        'activate/<uidb64>/<token>/',
        users.views.activate_user,
        name='activate_user'
    ),
    path(
        'users/', users.views.user_list, name='user_list'
    ),
    path(
        'users/<int:user_id>/', users.views.user_detail, name='user_detail'
    ),
    path(
        'profile/', users.views.user_profile, name='user_profile'
    ),
    path(
        'reset_login_attempts/<uidb64>/<token>/',
        users.views.reset_login_attempts,
        name='reset_login_attempts'
    ),
]
