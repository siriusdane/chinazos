import serpy
from django.contrib.auth.models import AnonymousUser
from WebPanel.models import PostInteraction
from WebPanel.serializers import ContextSerializer, SimpleProfileSerializer, PostCommentSerializer
LIKE = PostInteraction.INTERACTIONS.LIKE
DISLIKE = PostInteraction.INTERACTIONS.DISLIKE


class SimplePostSerializer(ContextSerializer):
    id = serpy.IntField()
    author = serpy.MethodField('get_author')
    title = serpy.StrField()
    content = serpy.StrField()
    points = serpy.IntField()
    liked = serpy.MethodField('get_liked')
    disliked = serpy.MethodField('get_disliked')

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


class PostSerializer(SimplePostSerializer):
    comments = serpy.MethodField('get_comments')

    def get_comments(self, obj):
        request = self.context.get('request')
        return PostCommentSerializer(obj.comments.all(), many=True, context={'request': request}).data
