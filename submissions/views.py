from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from projects.models import Project
from .forms import SubmissionForm
from notifications.models import Notification

@login_required
def submit_work(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if project.status != 'in_progress':

        return redirect(
            'project_details',
            id=project.id
        )

    if request.method == 'POST':

        form = SubmissionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            submission = form.save(
                commit=False
            )

            submission.project = project
            submission.freelancer = request.user
            submission.save()

            # Update project
            project.status = 'submitted'
            project.save()

            # Notify client
            Notification.objects.create(

                user=project.client,

                notification_type='submission',

                message=(
                    f'{request.user.first_name} '
                    f'submitted work for '
                    f'"{project.title}"'
                ),

                redirect_url=f'/projects/{project.id}/'
            )

            return redirect(
                'project_details',
                id=project.id
            )

    else:

        form = SubmissionForm()

    return render(
        request,
        'submissions/submit_work.html',
        {
            'form': form,
            'project': project
        }
    )

@login_required
def complete_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    # Only client
    if request.user != project.client:
        return redirect('home')

    # Only submitted project can complete
    if project.status != 'submitted':

        return redirect(
            'project_details',
            id=project.id
        )

    # COMPLETE ONLY HERE
    project.status = 'completed'
    project.save()

    return redirect(
        'create_review',
        project.id
    )