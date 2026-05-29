from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .forms import ReviewForm
from .models import Review
from projects.models import Project
from proposals.models import Proposal


@login_required
def create_review(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    # Only client
    if request.user != project.client:
        return redirect('home')

    # Prevent duplicate review
    if Review.objects.filter(
        project=project
    ).exists():

        return redirect(
            'project_details',
            id=project.id
        )

    accepted = Proposal.objects.filter(
        project=project,
        status='accepted'
    ).first()

    if request.method == 'POST':

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.project = project
            review.client = request.user
            review.freelancer = accepted.freelancer

            review.save()

            return redirect(
                'freelancer_profile',
                accepted.freelancer.id
            )

    else:

        form = ReviewForm()

    return render(
        request,
        'reviews/create_review.html',
        {
            'form': form,
            'project': project
        }
    )