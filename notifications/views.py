from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .models import Notification


# Notification List
@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'notifications/list.html',
        {
            'notifications': notifications
        }
    )


# Notification Click Redirect
@login_required
def notification_redirect(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user
    )

    # Mark as read
    notification.is_read = True
    notification.save()

    # Message notification
    if (
        notification.notification_type == 'message'
        and notification.conversation
    ):
        return redirect(
            'conversation_detail',
            notification.conversation.id
        )

    # Proposal + others
    if notification.redirect_url:
        return redirect(
            notification.redirect_url
        )

    return redirect(
        'notification_list'
    )