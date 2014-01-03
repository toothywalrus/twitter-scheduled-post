from django.conf.urls import patterns, url, include

from .views import WebPageViewSet, LinkViewSet
from .api import PageLinkList
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'webpages', WebPageViewSet)
router.register(r'links', LinkViewSet)

page_urls = patterns('', 
    url(r'^/(?P<pk>\d+)/links$', PageLinkList.as_view(), name='link-list'),
)

urlpatterns = patterns('',
    #url(r'^$', WebPageList.as_view(), name='webpage-list'),
    url(r'^',include(router.urls)),
    url(r'^pages', include(page_urls)),
)
