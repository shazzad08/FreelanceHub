from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


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