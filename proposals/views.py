from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Proposal
from .forms import ProposalForm
from projects.models import Project
from profiles.models import FreelanceProfile
from messaging.models import Conversation
from notifications.models import Notification


@login_required
def apply_to_project(request, id):   #for freelancer

    project = get_object_or_404(
        Project,
        id=id
    )

    if request.user == project.client:
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

            return redirect('project_details',id=project.id)

    else:

        form = ProposalForm()

    return render(request,'proposals/apply.html',{'form': form,'project': project})


@login_required
def proposal_dashboard(request):

    proposals = Proposal.objects.filter(
        project__client=request.user
    )

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
    
@login_required
def accept_proposal(request, id):

    proposal = get_object_or_404(
        Proposal,
        id=id
    )

    proposal.status = 'accepted'
    proposal.save()

    conversation, created = Conversation.objects.get_or_create(

        project=proposal.project,
        client=proposal.project.client,
        freelancer=proposal.freelancer
    )

    Notification.objects.create(

    user=proposal.freelancer,

    notification_type='proposal',

    message=(
        f'Your proposal for '
        f'"{proposal.project.title}" '
        f'was accepted.'
    )
)
    
    return redirect(
    'proposal_detail',
    proposal.id
)
    
@login_required
def reject_proposal(request, id):

    proposal = get_object_or_404(
        Proposal,
        id=id
    )

    proposal.status = 'rejected'
    proposal.save()

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

@login_required
def proposal_detail(request, id):

    proposal = get_object_or_404(
            Proposal,
            id=id
            )

    # Allow access if user is the client or the freelancer
    if request.user != proposal.project.client and request.user != proposal.freelancer:
        return redirect('home')

    # Fetch conversation if it exists
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
    
def freelancer_profile(request, id):
    
    profile = get_object_or_404(
        FreelanceProfile,
        user__id=id
    )

    return render(
        request,
        'proposals/freelancer_profile.html',
        {
            'profile_user': profile
        }
    )
    
@login_required
def freelancer_dashboard(request):

    proposals = Proposal.objects.filter(
        freelancer=request.user
    )

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