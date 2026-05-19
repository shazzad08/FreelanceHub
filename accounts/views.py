from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import User

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from django.urls import reverse_lazy

from django.contrib.auth.tokens import default_token_generator

from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from django.utils.encoding import (
    force_bytes,
    force_str
)

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string



def register_view(request):

    form = RegistrationForm()

    if request.method == 'POST':

        form = RegistrationForm(request.POST)  #Django fills the form with submitted data.

        if form.is_valid():

            user = form.save(commit=False)

            
            user.is_active = False

            user.save()

            # Generate secure token
            token = default_token_generator.make_token(user)

            # Encode user id
            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )

           
            confirm_link = (
                f"http://127.0.0.1:8000/"
                f"accounts/activate/{uid}/{token}/"
            )

          
            email_subject = "Confirm Your Email"

            email_body = render_to_string(
                'accounts/confirm_email.html',
                {
                    'confirm_link': confirm_link
                }
            )

           
            email = EmailMultiAlternatives(
                subject=email_subject,

                body='',

                to=[user.email]
            )

           
            email.attach_alternative(
                email_body,
                "text/html"
            )

            
            email.send()

            print("Verification email sent successfully")

           
            return redirect('login')

        else:

            print(form.errors)

    context = {
        'form': form
    }

    return render(
        request,
        'accounts/register.html',
        context
    )




def activate(request, uid, token):
    
    try:

        uid = force_str(
            urlsafe_base64_decode(uid)
        )
        print(uid)
        user = User.objects.get(pk=uid)

    except:

        user = None

    if (
        user is not None
        and default_token_generator.check_token(user, token)
    ):

        user.is_active = True

        user.is_verified = True

        user.save()

        return redirect('login')

    else:

        return redirect('register')




class UserLoginView(LoginView):

    template_name = 'accounts/login.html'

    def get_success_url(self):

        return reverse_lazy('home')




def logout_view(request):

    logout(request)

    return redirect('home')