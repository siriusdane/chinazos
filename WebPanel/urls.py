from django.conf.urls import url
from WebPanel.views import *

app_name = 'WebPanel'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login/service/$', LoginServiceView.as_view(), name='login-service'),
    url(r'^logout/service/$', LogoutServiceView.as_view(), name='logout-service'),
    url(r'^register/$', RegistrationView.as_view(), name='registration'),
    url(r'^register/service/$', RegistrationServiceView.as_view(), name='registration-service'),
    url(r'^posts/$', PostListView.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'^posts/(?P<pk>[0-9]+)/(?P<interaction>(like|dislike))/$', PostInteractionView.as_view(), name='post-interaction'),
    url(r'^posts/(?P<post_pk>[0-9]+)/comments/$', PostCommentListView.as_view(), name='comment-list'),
    url(r'^posts/(?P<post_pk>[0-9]+)/comments/(?P<pk>[0-9]+)/(?P<interaction>(like|dislike))/$', PostCommentInteractionView.as_view(), name='comment-interaction'),
    url(r'^comments/(?P<pk>[0-9]+)/replies/$', PostCommentReplyList.as_view(), name='reply-list'),
]
