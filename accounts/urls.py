from django.urls import path
from .views import register_view
from .views import UserLoginView,logout_view
from . import views


from accounts.forms import CustomPasswordResetForm
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/',UserLoginView.as_view() , name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uid>/<token>/',views.activate,name='activate'),
    
    path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        form_class=CustomPasswordResetForm,
        email_template_name='accounts/password_reset_email.txt',
        html_email_template_name='accounts/password_reset_email_html.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ),
    name='password_reset'
),
    
    path('password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        form_class=CustomPasswordResetForm,
        email_template_name='accounts/password_reset_email.txt',
        html_email_template_name='accounts/password_reset_email_html.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ),
    name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),



]
