from django.urls import path
from .views import register_view
from .views import UserLoginView,logout_view
from . import views



urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/',UserLoginView.as_view() , name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uid>/<token>/',views.activate,name='activate'),
    

]