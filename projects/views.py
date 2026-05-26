from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProjectForm
from .models import Project
from django.shortcuts import get_object_or_404

@login_required
def create_project(request):

    if request.method == 'POST':

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.client = request.user

            project.save()

            return redirect('project_list')

    else:

        form = ProjectForm()

    return render( request,'projects/create_project.html',{'form': form})


def project_list(request):
    
    projects= Project.objects.all()

    return render(request,'projects/project_list.html',{'projects': projects})



def project_details(request,id):

    project= get_object_or_404(Project,id=id)

    return render(request,'projects/project_details.html',{'project': project})
