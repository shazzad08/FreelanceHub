from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg

from .forms import (
    FreelancerProfileForm,
    ClientProfileForm
)

from .models import (
    FreelanceProfile,
    ClientProfile
)

from proposals.models import Proposal
from reviews.models import Review
from projects.models import Project


@login_required
def profile_view(request):
    user = request.user
    edit_mode = request.GET.get('edit')

    proposals = None
    reviews = None
    stats = {}
    skill_list = []

    # ================= FREELANCER =================
    if user.role == 'freelancer':
        profile, created = FreelanceProfile.objects.get_or_create(user=user)
        if profile.skills:
            if ',' in profile.skills:
                skill_list = [s.strip() for s in profile.skills.split(',') if s.strip()]
            else:
                skill_list = [s.strip() for s in profile.skills.split() if s.strip()]

        proposals = Proposal.objects.filter(
            freelancer=user
        ).select_related('project').order_by('-id')

        reviews = Review.objects.filter(
            freelancer=user
        ).select_related('project', 'client').order_by('-created_at')

        completed_projects_count = Proposal.objects.filter(
            freelancer=user,
            status='accepted',
            project__status='completed'
        ).count()

        earnings_data = Proposal.objects.filter(
            freelancer=user,
            status='accepted'
        ).aggregate(total=Sum('bid_amount'))

        total_earnings = earnings_data['total'] or 0

        rating_data = reviews.aggregate(avg=Avg('rating'))
        average_rating = round(rating_data['avg'] or 0, 1)

        total_proposals = Proposal.objects.filter(
            freelancer=user
        ).count()

        accepted_proposals = Proposal.objects.filter(
            freelancer=user,
            status='accepted'
        ).count()

        job_success = 0
        if total_proposals > 0:
            job_success = round(
                (accepted_proposals / total_proposals) * 100
            )

        stats = {
            'completed_projects_count': completed_projects_count,
            'total_earnings': total_earnings,
            'average_rating': average_rating,
            'job_success': job_success
        }

        form = FreelancerProfileForm(instance=profile)

        if request.method == 'POST':
            form = FreelancerProfileForm(
                request.POST,
                request.FILES,
                instance=profile
            )

            if form.is_valid():
                form.save()
                return redirect('profile')

    # ================= CLIENT =================
    else:
        profile, created = ClientProfile.objects.get_or_create(user=user)

        projects = Project.objects.filter(
            client=user
        )

        projects_posted_count = projects.count()

        active_projects_count = projects.filter(
            status__in=['open', 'in_progress', 'submitted']
        ).count()

        completed_projects_count = projects.filter(
            status='completed'
        ).count()

        total_spent_data = Proposal.objects.filter(
            project__client=user,
            status='accepted',
            project__status='completed'
        ).aggregate(total=Sum('bid_amount'))

        total_spent = total_spent_data['total'] or 0

        stats = {
            'projects_posted_count': projects_posted_count,
            'active_projects_count': active_projects_count,
            'completed_projects_count': completed_projects_count,
            'total_spent': total_spent
        }

        form = ClientProfileForm(instance=profile)

        if request.method == 'POST':
            form = ClientProfileForm(
                request.POST,
                request.FILES,
                instance=profile
            )

            if form.is_valid():
                form.save()
                return redirect('profile')

    context = {
        'profile': profile,
        'form': form,
        'edit_mode': edit_mode,
        'proposals': proposals,
        'reviews': reviews,
        'stats': stats,
        'skill_list': skill_list,
    }

    return render(
        request,
        'profiles/profile.html',
        context
    )


@login_required
def freelancer_list(request):
    freelancers = FreelanceProfile.objects.select_related('user').all()
    return render(
        request,
        'profiles/freelancer_list.html',
        {
            'freelancers': freelancers
        }
    )