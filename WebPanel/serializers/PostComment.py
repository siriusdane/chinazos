import serpy
from django.contrib.auth.models import AnonymousUser
from WebPanel.models import PostComment, PostCommentInteraction
from WebPanel.serializers import ContextSerializer, SimpleProfileSerializer
LIKE = PostCommentInteraction.INTERACTIONS.LIKE
DISLIKE = PostCommentInteraction.INTERACTIONS.DISLIKE


class PostCommentSerializer(ContextSerializer):
    id = serpy.IntField()
    author = serpy.MethodField('get_author')
    post_id = serpy.IntField()
    content = serpy.StrField()
    points = serpy.IntField()
    liked = serpy.MethodField('get_liked')
    disliked = serpy.MethodField('get_disliked')
    replies = serpy.MethodField('get_replies')

    def get_author(self, obj):
        return SimpleProfileSerializer(obj.profile).data

    def get_liked(self, obj):
        request = self.context.get('request')
        if not isinstance(request.user, AnonymousUser):
            return obj.interactions.filter(profile=request.user.profile, interaction=LIKE).count() > 0
        return False

    def get_disliked(self, obj):
        request = self.context.get('request')
        if not isinstance(request.user, AnonymousUser):
            return obj.interactions.filter(profile=request.user.profile, interaction=DISLIKE).count() > 0
        return False

    def get_replies(self, obj):
        query = PostComment.objects.filter(comment=obj).order_by('created')
        return PostCommentSerializer(query, many=True, context=self.context).data
