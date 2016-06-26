from django.db import models
from WebPanel.models import Profile, Post


class PostComment(models.Model):
    profile = models.ForeignKey(Profile, related_name='comments')
    post = models.ForeignKey(Post, related_name='comments')
    comment = models.ForeignKey('self', related_name='replies', null=True, blank=True)
    content = models.CharField(max_length=1000)
    points = models.IntegerField(blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'{0} - {1} on {2}'.format(self.created.strftime('%Y%m%dT%H%M%S'), self.profile.display,
                                          self.post.title)
