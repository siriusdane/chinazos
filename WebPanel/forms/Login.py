from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=4, max_length=16, widget=forms.PasswordInput)

    def clean(self):
        data = super(LoginForm, self).clean()
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is None:
            raise forms.ValidationError(_('Username and Password do not match'), code='invalid')
        elif not user.is_active:
            raise forms.ValidationError(_('Your user has been deactivated'), code='invalid')
        return data
