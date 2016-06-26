from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    display = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def email(self):
        return self.user.email

    def get_avatar(self):
        return self.avatar.url if self.avatar else static('WebPanel/img/profile.png')

    @classmethod
    def create_user(cls, username, password, email=None):
        user = User.objects.create_user(username, email, password)
        profile = Profile(user=user)
        profile.save()
        return profile

    def __unicode__(self):
        return u'{0}'.format(self.display)
