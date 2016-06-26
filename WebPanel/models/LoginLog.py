from django.db import models
from WebPanel.models import Profile


class LoginLog(models.Model):
    profile = models.ForeignKey(Profile)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.created.strftime('%Y%M%dT%H%M%S'), self.profile.display)
