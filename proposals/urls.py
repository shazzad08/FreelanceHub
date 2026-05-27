from django.urls import path
from . import views


urlpatterns = [

    path('apply/<int:id>/',views.apply_to_project,name='apply_to_project'),

    path('dashboard/',views.proposal_dashboard,name='proposal_dashboard'),

    path('accept/<int:id>/',views.accept_proposal, name='accept_proposal'),

    path('reject/<int:id>/',views.reject_proposal,name='reject_proposal'),

    path('detail/<int:id>/',views.proposal_detail,name='proposal_detail'),
    
    path('freelancer/<int:id>/',views.freelancer_profile,name='freelancer_profile'),
    
    path('freelancer-dashboard/',views.freelancer_dashboard,name='freelancer_dashboard'),

]