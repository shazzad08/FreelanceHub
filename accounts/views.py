from django.shortcuts import render, redirect
from .forms import RegistrationForm


def register_view(request):

    form = RegistrationForm()

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login.html')

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)