from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import ProjectForm
from .models import Project
from categories.models import Category
from profiles.models import ClientProfile
from accounts.models import User
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
    
    categories = Category.objects.all()

    
    if request.user.role == 'freelancer':

        projects = Project.objects.all().order_by('-id')

    else:

        projects = Project.objects.filter(
            client=request.user
        ).order_by('-id')

    # Search
    query = request.GET.get('q')

    if query:

        projects = projects.filter(
            title__icontains=query
        )

    # Category Filter
    category_id = request.GET.get('category')

    if category_id:

        projects = projects.filter(
            category_id=category_id
        )

    # Budget Sort
    sort = request.GET.get('sort')

    if sort == 'low':

        projects = projects.order_by(
            'budget'
        )

    elif sort == 'high':

        projects = projects.order_by(
            '-budget'
        )

    return render(request,'projects/project_list.html',{'projects': projects,'categories': categories})



def project_details(request,id):

    project= get_object_or_404(Project,id=id)

    return render(request,'projects/project_details.html',{'project': project})



@login_required
def edit_project(request, id):

    project = get_object_or_404(
        Project,
        id=id,
        client=request.user
    )

    if request.method == 'POST':

        form = ProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect('project_list')

    else:

        form = ProjectForm(instance=project)

    return render(
        request,
        'projects/edit_project.html',
        {'form': form,
        'project': project}
    )




@login_required
def delete_project(request, id):

    project = get_object_or_404(
        Project,
        id=id,
        client=request.user
    )

    if request.method == 'POST':

        project.delete()

        return redirect('project_list')

    return redirect(
        'project_details',
        id=project.id
    )




def client_profile(request, id):
    # Check if user exists
    user = get_object_or_404(User, id=id)
    
    # Check if user is a client
    if user.role != 'client':
        raise Http404(f"User is a {user.role}, not a client.")
    
    # Get client profile
    profile = get_object_or_404(
        ClientProfile,
        user__id=id
    )

    return render(request,'projects/client_profile.html',{'profile_user': profile})