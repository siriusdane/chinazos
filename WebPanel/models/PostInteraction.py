from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from WebPanel.models import Profile, Post
from WebPanel.utilities import enum, enum_name


class PostInteraction(models.Model):
    INTERACTIONS = enum(LIKE=1, DISLIKE=2)
    INTERACTIONS_CHOICES = sorted([(v, k) for k, v in INTERACTIONS.__dict__.items() if not k.startswith('__')])

    profile = models.ForeignKey(Profile, related_name='postInteractions')
    post = models.ForeignKey(Post, related_name='interactions')
    interaction = models.IntegerField(choices=INTERACTIONS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def get_interaction(self):
        return enum_name(PostInteraction.INTERACTIONS_CHOICES, self.interaction)

    def __unicode__(self):
        return u'{0} - {1} {2} by {3}'.format(self.created.strftime('%Y%m%dT%H%M%S'), self.post.title,
                                              self.get_interaction(), self.profile.display)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.interaction == PostInteraction.INTERACTIONS.LIKE:
            self.post.points += 1
        elif self.interaction == PostInteraction.INTERACTIONS.DISLIKE:
            self.post.points -= 1
        self.post.save()
        super(PostInteraction, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.interaction == PostInteraction.INTERACTIONS.LIKE:
            self.post.points -= 1
        elif self.interaction == PostInteraction.INTERACTIONS.DISLIKE:
            self.post.points += 1
        self.post.save()
        super(PostInteraction, self).delete(using, keep_parents)
