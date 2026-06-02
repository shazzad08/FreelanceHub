from django.shortcuts import render
from projects.models import Project


def home(request):
    latest_projects = Project.objects.filter(status='open').order_by('-created_at')[:6]
    
    context = {
        'latest_projects': latest_projects
    }
    
    return render(request, 'home.html', context)