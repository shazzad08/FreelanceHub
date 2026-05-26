from django.urls import path
from . import views

urlpatterns = [

    path('create/',views.create_project,name='create_project'),
    path('',views.project_list,name='project_list'),
    path('<int:id>/',views.project_details,name='project_details'),
    path('<int:id>/edit/', views.edit_project, name='edit_project'),
    path('<int:id>/delete/',views.delete_project,name='delete_project'),
    path('profile/<int:id>/',views.client_profile,name='client_profile'),

]