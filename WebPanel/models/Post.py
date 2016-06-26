from django.db import models
from WebPanel.models import Profile


class Post(models.Model):
    profile = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    points = models.IntegerField(blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{0} - {1}: {2}'.format(self.created.strftime('%Y%m%dT%H:%M:%S'), self.profile.display,
                                        self.title)
