from django.urls import path
from . import views

urlpatterns = [

    # Freelancer submit work
    path(
        'submit/<int:project_id>/',
        views.submit_work,
        name='submit_work'
    ),

    # Client mark complete
    path(
        'complete/<int:project_id>/',
        views.complete_project,
        name='complete_project'
    ),

]