from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from WebPanel.models import Profile


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    email = forms.EmailField(required=False)
    password = forms.CharField(min_length=8, max_length=16, widget=forms.PasswordInput)
    confirmation = forms.CharField(min_length=8, max_length=16, widget=forms.PasswordInput)
    display = forms.CharField(min_length=3, max_length=50)

    def create_user(self):
        data = self.cleaned_data
        user = User.objects.create_user(username=data.get('username'), password=data.get('password'),
                                        email=data.get('email'))
        profile = Profile(user=user, display=data.get('display'))
        profile.save()
        return profile

    def clean_username(self):
        value = self.cleaned_data['username']
        if User.objects.filter(username=value).count() > 0:
            raise forms.ValidationError(_('Username is already used'), code='invalid')
        return value

    def clean_email(self):
        value = self.cleaned_data['email']
        if value and User.objects.filter(email=value).count() > 0:
            raise forms.ValidationError(_('Email is already used'), code='invalid')
        return value

    def clean_display(self):
        value = self.cleaned_data['display']
        if Profile.objects.filter(display=value).count() > 0:
            raise forms.ValidationError(_('Display name is already used'), code='invalid')
        return value

    def clean(self):
        data = super(RegistrationForm, self).clean()
        if data.get('password') != data.get('confirmation'):
            raise forms.ValidationError(_('Password and Confirmation must match'), code='invalid')
        return data
