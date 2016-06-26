from django.utils.safestring import mark_safe
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from WebPanel.models import Profile, Post, PostInteraction
from WebPanel.forms import PostForm
from WebPanel.serializers import SimplePostSerializer, PostSerializer
from WebPanel.utilities import paginate_results
import json
LIKE = PostInteraction.INTERACTIONS.LIKE
DISLIKE = PostInteraction.INTERACTIONS.DISLIKE


class PostListView(View):
    @staticmethod
    def get(request):
        query = Post.objects.all().order_by('-created')
        page, size = request.GET.get('page', '1'), request.GET.get('size', '25')
        response = paginate_results(query, SimplePostSerializer, {'request': request}, page=int(page), size=int(size))
        return HttpResponse(json.dumps(response), status=200, content_type='application/json')

    @staticmethod
    def post(request):
        form = PostForm(request.POST, prefix='post')
        if form.is_valid():
            post = form.save(commit=False)
            post.profile = request.user.profile
            post.save()
            return HttpResponse(json.dumps(SimplePostSerializer(post, context={'request': request}).data),
                                status=201, content_type='application/json')
        print form.errors
        return HttpResponse(json.dumps({'errors': form.errors}), status=400)


class PostDetailView(View):
    @staticmethod
    def get(request, pk):
        post = Post.objects.get(pk=pk)
        objects = {'post': mark_safe(json.dumps(PostSerializer(post, context={'request': request}).data))}
        return render(request, 'WebPanel/Post.html', objects)


class PostInteractionView(View):
    @staticmethod
    def post(request, pk, interaction):
        profile = Profile.objects.get(user=request.user)
        post = Post.objects.get(pk=pk)
        interaction = LIKE if interaction == 'like' else DISLIKE
        post = PostInteractionView._delete_previous(profile, post, interaction)
        PostInteraction.objects.get_or_create(profile=profile, post=post, interaction=interaction)
        return HttpResponse(json.dumps(SimplePostSerializer(post, context={'request': request}).data), status=202,
                            content_type='application/json')

    @staticmethod
    def _delete_previous(profile, post, interaction):
        if interaction == LIKE:
            posts = PostInteraction.objects.filter(profile=profile, post=post, interaction=DISLIKE)
        elif interaction == DISLIKE:
            posts = PostInteraction.objects.filter(profile=profile, post=post, interaction=LIKE)
        else:
            posts = []
        for i in posts:
            i.delete()
        return Post.objects.get(pk=post.pk)
