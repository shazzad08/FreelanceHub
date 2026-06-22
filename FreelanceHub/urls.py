from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from accounts.forms import CustomPasswordResetForm
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', include('core.urls')),

    path('admin/', admin.site.urls),

    path('accounts/', include("accounts.urls")),

    path('profile/', include('profiles.urls')),

    path('projects/',include('projects.urls')),

    path('proposals/',include('proposals.urls')),

    path('messages/',include('messaging.urls')),
    
    path('notifications/',include('notifications.urls')),
    
    path('submissions/',include('submissions.urls')),
    path('reviews/',include('reviews.urls')),
    
    path('password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        form_class=CustomPasswordResetForm
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


# Static Files
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

# Media Files
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)