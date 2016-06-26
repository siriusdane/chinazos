from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.views.generic import View
from WebPanel.forms import RegistrationForm


class RegistrationView(View):
    @staticmethod
    def get(request):
        objects = {
            'registration_form': RegistrationForm(prefix='registration')
        }
        return render(request, 'WebPanel/Registration.html', objects)

    @staticmethod
    def post(request):
        form = RegistrationForm(request.POST, prefix='registration')
        if form.is_valid():
            form.create_user()
            return redirect('WebPanel:login')
        print(form.errors)
        return render(request, 'WebPanel/Registration.html', {'registration_form': form})


class RegistrationServiceView(View):
    @staticmethod
    def post(request):
        form = RegistrationForm(request.POST, prefix='registration')
        if form.is_valid():
            profile = form.create_user()
            login(request, profile.user)
            return HttpResponse(status=200)
        print(form.errors)
        return HttpResponse(status=400)
