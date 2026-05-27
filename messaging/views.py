from django.shortcuts import (render,get_object_or_404,redirect)
from django.contrib.auth.decorators import login_required

from .models import Conversation
from .forms import MessageForm
from notifications.models import Notification


@login_required
def conversation_detail(request, id):

    conversation = get_object_or_404(
        Conversation,
        id=id
    )

    # Security Check

    if request.user not in [

        conversation.client,
        conversation.freelancer

    ]:

        return redirect(
            'home'
        )

    # Send Message

    if request.method == 'POST':

        form = MessageForm(
            request.POST
        )

        if form.is_valid():

            message = form.save(
                commit=False
            )

            message.conversation = conversation
            message.sender = request.user

            message.save()

            # Find receiver

            if request.user == conversation.client:

                receiver = conversation.freelancer

            else:

                receiver = conversation.client

            # Create notification

            Notification.objects.create(

                user=receiver,

                notification_type='message',

                conversation=conversation,

                message=(
                    f'{request.user.first_name} '
                    f'sent you a message about '
                    f'"{conversation.project.title}".'
                )
            )

            return redirect(
                'conversation_detail',
                id=conversation.id
            )

    else:

        form = MessageForm()

    return render(
        request,
        'messaging/conversation.html',
        {
            'conversation': conversation,
            'form': form
        }
    )