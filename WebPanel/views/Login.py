from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from WebPanel.forms import LoginForm


class LoginView(View):
    @staticmethod
    def get(request):
        logout(request)
        objects = {'login_form': LoginForm(prefix='login')}
        return render(request, 'WebPanel/Login.html', objects)

    @staticmethod
    def post(request):
        form = LoginForm(request.POST, prefix='login')
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)
            return redirect('WebPanel:home')
        print(form.errors)
        return render(request, 'WebPanel/Login.html', {'login_form': form})


class LoginServiceView(View):
    @staticmethod
    def post(request):
        form = LoginForm(request.POST, prefix='login')
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)
            return HttpResponse(status=200)
        return HttpResponse(status=400)


class LogoutServiceView(View):
    @staticmethod
    def post(request):
        logout(request)
        return HttpResponse(status=200)
