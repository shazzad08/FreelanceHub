from django.urls import path

from .views import profile_view
from .views import freelancer_list

urlpatterns = [

    path('',profile_view,name='profile'),
    path('freelancers/',freelancer_list,name='freelancer_list'),

]