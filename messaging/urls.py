from django.urls import path
from . import views

urlpatterns = [

    path(
        '<int:id>/',
        views.conversation_detail,
        name='conversation_detail'
    ),

]