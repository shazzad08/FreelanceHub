from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import ProjectForm
from .models import Project

from categories.models import Category
from profiles.models import ClientProfile
from accounts.models import User
from proposals.models import Proposal
from messaging.models import Conversation
from submissions.models import Submission
from profiles.models import FreelanceProfile
from django.db.models import Q
from django.http import JsonResponse






@login_required
def create_project(request):

    if request.method == 'POST':

        form = ProjectForm(
            request.POST
        )

        if form.is_valid():

            project = form.save(
                commit=False
            )

            project.client = request.user
            project.save()

            return redirect(
                'project_list'
            )

    else:

        form = ProjectForm()

    return render(
        request,
        'projects/create_project.html',
        {
            'form': form
        }
    )


def project_list(request):

    categories = Category.objects.all()
    total_projects = Project.objects.count()
    freelancer_count = User.objects.filter(role='freelancer').count()

    # Search query
    query = request.GET.get('q', '').strip()

    # Base queryset depending on role
    if query:
        # Search is global
        projects = Project.objects.all().order_by('-id')
    elif (
        request.user.is_authenticated
        and
        request.user.role == 'client'
    ):
        projects = Project.objects.filter(
            client=request.user
        ).order_by('-id')
    else:
        projects = Project.objects.all().order_by(
            '-id'
        )

    # Search filtering
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Category filter
    category_id = request.GET.get(
        'category'
    )

    if category_id and category_id.isdigit():

        projects = projects.filter(
            category_id=category_id
        )

    # Budget sort
    sort = request.GET.get('sort')

    if sort == 'low':

        projects = projects.order_by(
            'budget'
        )

    elif sort == 'high':

        projects = projects.order_by(
            '-budget'
        )

    return render(
        request,
        'projects/project_list.html',
        {
            'projects': projects,
            'categories': categories,
            'total_projects': total_projects,
            'freelancer_count': freelancer_count,
            'selected_category': category_id,
            'selected_sort': sort,
            'query': query,
        }
    )



@login_required
def project_details(request, id):

    project = get_object_or_404(
        Project,
        id=id
    )

    proposals = Proposal.objects.filter(
        project=project
    )

    accepted_proposal = proposals.filter(
        status='accepted'
    ).first()

    conversation = None

    if accepted_proposal:

        conversation = Conversation.objects.filter(
            project=project,
            freelancer=accepted_proposal.freelancer
        ).first()

    # Submission
    submission = Submission.objects.filter(
        project=project
    ).first()

    # Check if freelancer already applied
    already_applied = False

    if (
        request.user.is_authenticated
        and request.user != project.client
    ):
        already_applied = Proposal.objects.filter(
            project=project,
            freelancer=request.user
        ).exists()

    return render(
        request,
        'projects/project_details.html',
        {
            'project': project,
            'proposals': proposals,
            'accepted_proposal': accepted_proposal,
            'conversation': conversation,
            'submission': submission,
            'already_applied': already_applied,
        }
    )


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

            return redirect(
                'project_list'
            )

    else:

        form = ProjectForm(
            instance=project
        )

    return render(
        request,
        'projects/edit_project.html',
        {
            'form': form,
            'project': project
        }
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

        return redirect(
            'project_list'
        )

    return redirect(
        'project_details',
        id=project.id
    )



def client_profile(request, id):

    user = get_object_or_404(
        User,
        id=id
    )

    if user.role != 'client':

        raise Http404(
            f'User is a {user.role}, not a client.'
        )

    profile = get_object_or_404(
        ClientProfile,
        user__id=id
    )

    return render(
        request,
        'projects/client_profile.html',
        {
            'profile_user': profile
        }
    )
    
    
@login_required
def category_freelancers(request, slug):

    freelancers = FreelanceProfile.objects.filter(
        category__slug=slug
    )

    return render(
        request,
        'category/freelancer_list.html',
        {
            'freelancers': freelancers,
            'slug': slug
        }
    )

def category_projects(request, slug):

    projects = Project.objects.filter(
        category__slug=slug
    )

    context = {
        'projects': projects,
        'category_slug': slug
    }

    return render(
        request,
        'category/project_list.html',
        context
    )
    


def home(request):
    
    categories = Category.objects.all()

    # Base queryset
    projects = Project.objects.all().order_by(
        '-id'
    )

    # Search filter
    query = request.GET.get('q')

    if query:
        projects = projects.filter(
            title__icontains=query
        )

    # Category filter
    category_id = request.GET.get(
        'category'
    )

    if category_id:
        projects = projects.filter(
            category_id=category_id
        )

    # Budget sort
    sort = request.GET.get('sort')

    if sort == 'low':
        projects = projects.order_by(
            'budget'
        )

    elif sort == 'high':
        projects = projects.order_by(
            '-budget'
        )

    # Homepage latest cards
    latest_projects = projects[:4]

    context = {
        'latest_projects': latest_projects,
        'categories': categories,
    }

    return render(
        request,
        'home.html',
        context
    )
    
    

def search_suggestions(request):
    query = request.GET.get('q', '').strip() or request.GET.get('term', '').strip()
    suggestions = []
    seen = set()

    if query:
        # Category suggestions first (usually higher level)
        categories = Category.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True).distinct()[:10]

        # Project title suggestions
        projects = Project.objects.filter(
            title__icontains=query
        ).values_list('title', flat=True).distinct()[:10]

        for name in list(categories) + list(projects):
            name_stripped = name.strip()
            name_lower = name_stripped.lower()
            if name_lower not in seen:
                seen.add(name_lower)
                suggestions.append(name_stripped)

    return JsonResponse(suggestions[:10], safe=False)