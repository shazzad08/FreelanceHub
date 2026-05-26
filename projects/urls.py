from django.urls import path
from . import views

urlpatterns = [

    path('create/',views.create_project,name='create_project'),
    path('',views.project_list,name='project_list'),
    path('<int:id>/',views.project_details,name='project_details')

]