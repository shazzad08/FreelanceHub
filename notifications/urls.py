from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.notification_list,
        name='notification_list'
    ),

    path(
        'redirect/<int:id>/',
        views.notification_redirect,
        name='notification_redirect'
    ),

]