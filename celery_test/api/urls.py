from django.conf.urls import patterns, url, include

from .views import WebPageViewSet, LinkViewSet
from .api import PageLinkList
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'webpages', WebPageViewSet)
router.register(r'links', LinkViewSet)

# user_urls = patterns('',
#     url(r'^/(?P<username>[0-9a-zA-Z_-]+)/posts$', UserPostList.as_view(), name='userpost-list'),
#     url(r'^/(?P<username>[0-9a-zA-Z_-]+)$', UserDetail.as_view(), name='user-detail'),
#     url(r'^$', UserList.as_view(), name='user-list')
# )

# post_urls = patterns('',
#     url(r'^/(?P<pk>\d+)/photos$', PostPhotoList.as_view(), name='postphoto-list'),
#     url(r'^/(?P<pk>\d+)$', PostDetail.as_view(), name='post-detail'),
#     url(r'^$', PostList.as_view(), name='post-list')
# )

# photo_urls = patterns('',
#     url(r'^/(?P<pk>\d+)$', PhotoDetail.as_view(), name='photo-detail'),
#     url(r'^$', PhotoList.as_view(), name='photo-list')
# )

page_urls = patterns('', 
    url(r'^/(?P<pk>\d+)/links$', PageLinkList.as_view(), name='link-list'),
)

urlpatterns = patterns('',
    #url(r'^$', WebPageList.as_view(), name='webpage-list'),
    url(r'^',include(router.urls)),
    url(r'^pages', include(page_urls)),
)
