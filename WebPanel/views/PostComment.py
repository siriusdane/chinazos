from django.views.generic import View
from django.http import HttpResponse
from WebPanel.models import Profile, PostComment, PostCommentInteraction
from WebPanel.forms import PostCommentForm
from WebPanel.serializers import PostCommentSerializer
from WebPanel.utilities import paginate_results
import json
LIKE = PostCommentInteraction.INTERACTIONS.LIKE
DISLIKE = PostCommentInteraction.INTERACTIONS.DISLIKE


class PostCommentListView(View):
    @staticmethod
    def get(request, post_pk):
        query = PostComment.objects.filter(post_id=post_pk, comment=None).order_by('-created')
        page, size = request.GET.get('page', '1'), request.GET.get('size', '10')
        response = paginate_results(query, PostCommentSerializer, {'request': request}, int(page), int(size))
        return HttpResponse(json.dumps(response), content_type='application/json')

    @staticmethod
    def post(request, post_pk):
        form = PostCommentForm(request.POST, prefix='comment')
        if form.is_valid():
            comment = form.save(commit=False)
            comment.profile = request.user.profile
            comment.post_id = post_pk
            comment.save()
            return HttpResponse(json.dumps(PostCommentSerializer(comment, context={'request': request}).data),
                                status=201, content_type='application/json')
        print form.errors
        return HttpResponse(json.dumps({'errors': form.errors}), status=400, content_type='application/json')


class PostCommentInteractionView(View):
    @staticmethod
    def post(request, post_pk, pk, interaction):
        profile = Profile.objects.get(user=request.user)
        comment = PostComment.objects.get(pk=pk)
        interaction = LIKE if interaction == 'like' else DISLIKE
        comment = PostCommentInteractionView._delete_previous(profile, comment, interaction)
        PostCommentInteraction.objects.get_or_create(profile=profile, comment=comment, interaction=interaction)
        return HttpResponse(json.dumps(PostCommentSerializer(comment, context={'request': request}).data),
                            status=202, content_type='application/json')

    @staticmethod
    def _delete_previous(profile, comment, interaction):
        if interaction == LIKE:
            interactions = PostCommentInteraction.objects.filter(profile=profile, comment=comment, interaction=DISLIKE)
        elif interaction == DISLIKE:
            interactions = PostCommentInteraction.objects.filter(profile=profile, comment=comment, interaction=LIKE)
        else:
            interactions = []
        for i in interactions:
            i.delete()
        return PostComment.objects.get(pk=comment.pk)


class PostCommentReplyList(View):
    @staticmethod
    def get(request, pk):
        query = PostComment.objects.filter(comment_id=pk).order_by('created')
        page, size = request.GET.get('page', '1'), request.GET.get('size', '10')
        response = paginate_results(query, PostCommentSerializer, {'request': request}, int(page), int(size))
        return HttpResponse(json.dumps(response), content_type='application/json')
