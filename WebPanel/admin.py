from django.contrib import admin
from WebPanel.models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(LoginLog)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostInteraction)
admin.site.register(PostCommentInteraction)
