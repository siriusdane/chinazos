from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from WebPanel.models import Profile, PostComment
from WebPanel.utilities import enum, enum_name


class PostCommentInteraction(models.Model):
    INTERACTIONS = enum(LIKE=1, DISLIKE=2)
    INTERACTIONS_CHOICES = sorted([(v, k) for k, v in INTERACTIONS.__dict__.items() if not k.startswith('__')])

    profile = models.ForeignKey(Profile, related_name='comment_interactions', on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, related_name='interactions', on_delete=models.CASCADE)
    interaction = models.IntegerField(choices=INTERACTIONS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def get_interaction(self):
        return enum_name(PostCommentInteraction.INTERACTIONS_CHOICES, self.interaction)

    def __unicode__(self):
        return u'{0} - {1} by {2}'.format(self.created.strftime('%Y%m%dT%H%M%S'),  self.get_interaction(),
                                          self.profile.display)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.interaction == PostCommentInteraction.INTERACTIONS.LIKE:
            self.comment.points += 1
        elif self.interaction == PostCommentInteraction.INTERACTIONS.DISLIKE:
            self.comment.points -= 1
        self.comment.save()
        super(PostCommentInteraction, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.interaction == PostCommentInteraction.INTERACTIONS.LIKE:
            self.comment.points -= 1
        elif self.interaction == PostCommentInteraction.INTERACTIONS.DISLIKE:
            self.comment.points += 1
        self.comment.save()
        super(PostCommentInteraction, self).delete(using, keep_parents)

