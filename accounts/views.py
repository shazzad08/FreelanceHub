from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

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

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):

    next_page = reverse_lazy('home')