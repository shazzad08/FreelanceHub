from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Proposal
from .forms import ProposalForm
from projects.models import Project
from profiles.models import FreelanceProfile

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
def proposal_dashboard(request):          #for client

    proposals = Proposal.objects.filter(
        project__client=request.user
    )

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

    return redirect(
        'proposal_dashboard'
    )
    
@login_required
def reject_proposal(request, id):

    proposal = get_object_or_404(
        Proposal,
        id=id
    )

    proposal.status = 'rejected'

    proposal.save()

    return redirect(
        'proposal_dashboard'
    )
    
    
@login_required
def proposal_detail(request, id):

    proposal = get_object_or_404(
        Proposal,
        id=id,
        project__client=request.user
    )

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