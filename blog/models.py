from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from profile.models import UserProfile


class PostComment(models.Model):
    comments = models.Manager()
    sent_time = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, related_name="comment", default=0, blank=True)
    like = models.IntegerField(default=0)
    users_like = models.ManyToManyField(User, related_name='users_like', default=None, blank=True)
    # dislike = models.IntegerField(default=0)

    def __unicode__(self):
        return "{0}: {1}".format(self.user.username, self.comment)


class BlogPost(models.Model):
    posts = models.Manager()
    author = models.ForeignKey(User)
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField('PostComment', related_name='posts', default=None, blank=True)

    class Meta:
        ordering = ('-timestamp',)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'timestamp')

    class Meta:
        ordering = ('-timestamp')





class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'phone', 'about_user')

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

