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

]


# Media Files
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)