from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .models import Proposal
from .forms import ProposalForm

from projects.models import Project
from profiles.models import FreelanceProfile
from messaging.models import Conversation
from notifications.models import Notification
from reviews.models import Review


# APPLY TO PROJECT
@login_required
def apply_to_project(request, id):

    project = get_object_or_404(
        Project,
        id=id
    )

    # Prevent client applying own project
    if request.user == project.client:

        return redirect(
            'project_details',
            id=project.id
        )

    # Prevent duplicate apply
    already_applied = Proposal.objects.filter(
        project=project,
        freelancer=request.user
    ).exists()

    if already_applied:

        return redirect(
            'project_details',
            id=project.id
        )

    if request.method == 'POST':

        form = ProposalForm(
            request.POST
        )

        if form.is_valid():

            proposal = form.save(
                commit=False
            )

            proposal.project = project
            proposal.freelancer = request.user
            proposal.save()

            return redirect(
                'project_details',
                id=project.id
            )

    else:

        form = ProposalForm()

    return render(
        request,
        'proposals/apply.html',
        {
            'form': form,
            'project': project
        }
    )


# CLIENT DASHBOARD
@login_required
def proposal_dashboard(request):

    proposals = Proposal.objects.filter(
        project__client=request.user
    ).order_by('-id')

    for proposal in proposals:

        proposal.conversation = Conversation.objects.filter(
            project=proposal.project,
            freelancer=proposal.freelancer
        ).first()

    return render(
        request,
        'proposals/dashboard.html',
        {
            'proposals': proposals
        }
    )


# ACCEPT PROPOSAL
@login_required
def accept_proposal(request, id):

    proposal = get_object_or_404(
        Proposal,
        id=id
    )

    # Only client
    if request.user != proposal.project.client:
        return redirect('home')

    # Reject others
    Proposal.objects.filter(
        project=proposal.project
    ).exclude(
        id=proposal.id
    ).update(
        status='rejected'
    )

    # Accept
    proposal.status = 'accepted'
    proposal.save()

    # Project -> in progress
    project = proposal.project
    project.status = 'in_progress'
    project.save()

    # Conversation
    Conversation.objects.get_or_create(
        project=project,
        client=project.client,
        freelancer=proposal.freelancer
    )

    # Notification
    Notification.objects.create(
        user=proposal.freelancer,
        notification_type='proposal',
        message=(
            f'Your proposal for '
            f'"{project.title}" '
            f'was accepted.'
        )
    )

    return redirect(
        'proposal_detail',
        proposal.id
    )


# REJECT PROPOSAL
@login_required
def reject_proposal(request, id):

    proposal = get_object_or_404(
        Proposal,
        id=id
    )

    if request.user != proposal.project.client:
        return redirect('home')

    proposal.status = 'rejected'
    proposal.save()

    # Reset project if no accepted proposal
    accepted_exists = Proposal.objects.filter(
        project=proposal.project,
        status='accepted'
    ).exists()

    if not accepted_exists:

        proposal.project.status = 'open'
        proposal.project.save()

    Notification.objects.create(
        user=proposal.freelancer,
        notification_type='proposal',
        message=(
            f'Your proposal for '
            f'"{proposal.project.title}" '
            f'was rejected.'
        )
    )

    return redirect(
        'proposal_detail',
        proposal.id
    )


# PROPOSAL DETAIL
@login_required
def proposal_detail(request, id):

    proposal = get_object_or_404(
        Proposal,
        id=id
    )

    if (
        request.user != proposal.project.client
        and
        request.user != proposal.freelancer
    ):

        return redirect('home')

    proposal.conversation = Conversation.objects.filter(
        project=proposal.project,
        freelancer=proposal.freelancer
    ).first()

    return render(
        request,
        'proposals/proposal_detail.html',
        {
            'proposal': proposal
        }
    )


# FREELANCER PROFILE + REVIEWS
def freelancer_profile(request, id):

    profile = get_object_or_404(
        FreelanceProfile,
        user__id=id
    )

    reviews = Review.objects.filter(
        freelancer=profile.user
    ).order_by('-created_at')

    avg_rating = 0

    if reviews.exists():

        total = sum(
            review.rating
            for review in reviews
        )

        avg_rating = round(
            total / reviews.count(),
            1
        )

    return render(
        request,
        'proposals/freelancer_profile.html',
        {
            'profile_user': profile,
            'reviews': reviews,
            'avg_rating': avg_rating
        }
    )


# FREELANCER DASHBOARD
@login_required
def freelancer_dashboard(request):

    proposals = Proposal.objects.filter(
        freelancer=request.user
    ).order_by('-id')

    for proposal in proposals:

        proposal.conversation = Conversation.objects.filter(
            project=proposal.project,
            freelancer=proposal.freelancer
        ).first()

    return render(
        request,
        'proposals/freelancer_dashboard.html',
        {
            'proposals': proposals
        }
    )