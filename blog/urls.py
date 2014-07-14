from django.conf.urls import patterns, url, include
from django.views.generic.detail import View
from blog.views import *
from django.contrib.auth.models import User

urlpatterns=patterns('',
                         #url(r'^$', archive),
                         url(r'^(?P<user_id>\d+)/page/(?P<page>\d+)?/?$', PostListView.as_view(template_name='archive.html'), name='list' ),
                         url(r'^post/add/?', PostAdd.as_view(), name="add_post"),
                         url(r'^post/(?P<pk>\d+)/change/$', PostUpdate.as_view(), name="change_post"),
                         url(r'^post/(?P<pk>\d+)/delete/$', PostDelete.as_view(), name="delete_post"),
                         url(r'^post/(?P<pk>\d+)/$', PostView.as_view(), name="detail_post"),
                         url(r'like/(\d+)/$', LikeRequest, name='like'),




)
