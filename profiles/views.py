from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import uuid

from .forms import (
    FreelancerProfileForm,
    ClientProfileForm
)

from .models import (
    FreelanceProfile,
    ClientProfile
)

from proposals.models import Proposal
from utils.supabase_helper import supabase


@login_required
def profile_view(request):

    user = request.user
    edit_mode = request.GET.get('edit')

    proposals = None

    # Freelancer
    if user.role == 'freelancer':

        profile, created = FreelanceProfile.objects.get_or_create(
            user=user
        )

        proposals = Proposal.objects.filter(
            freelancer=user
        ).order_by('-id')

        form = FreelancerProfileForm(
            instance=profile
        )

        if request.method == 'POST':

            form = FreelancerProfileForm(
                request.POST,
                request.FILES,
                instance=profile
            )

            if form.is_valid():

                profile = form.save(commit=False)

                if request.FILES.get('profile_image'):
                    image = request.FILES['profile_image']
                    filename = f"{uuid.uuid4()}_{image.name}"

                    supabase.storage.from_("profile-images").upload(
                        filename,
                        image.read()
                    )

                    public_url = supabase.storage.from_(
                        "profile-images"
                    ).get_public_url(filename)

                    profile.profile_image_url = public_url

                profile.save()
                return redirect('profile')

    # Client
    else:

        profile, created = ClientProfile.objects.get_or_create(
            user=user
        )

        form = ClientProfileForm(
            instance=profile
        )

        if request.method == 'POST':

            form = ClientProfileForm(
                request.POST,
                request.FILES,
                instance=profile
            )

            if form.is_valid():

                profile = form.save(commit=False)

                if request.FILES.get('company_logo'):
                    image = request.FILES['company_logo']
                    filename = f"{uuid.uuid4()}_{image.name}"

                    supabase.storage.from_("profile-images").upload(
                        filename,
                        image.read()
                    )

                    public_url = supabase.storage.from_(
                        "profile-images"
                    ).get_public_url(filename)

                    profile.company_logo_url = public_url

                profile.save()
                return redirect('profile')

    context = {
        'profile': profile,
        'form': form,
        'edit_mode': edit_mode,
        'proposals': proposals,
    }

    return render(
        request,
        'profiles/profile.html',
        context
    )


def freelancer_list(request):

    freelancers = FreelanceProfile.objects.filter(
        user__role='freelancer',
        user__is_verified=True
    ).select_related('user')

    return render(
        request,
        'profiles/freelancer_list.html',
        {
            'freelancers': freelancers
        }
    )