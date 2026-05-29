from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/<int:project_id>/',
        views.create_review,
        name='create_review'
    ),

]