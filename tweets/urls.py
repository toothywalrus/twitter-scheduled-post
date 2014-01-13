from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from .views import TweetViewSet, TimedTweetViewSet, \
    PeriodicTweetViewSet, PostTweetSetViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'tweets', TweetViewSet)
router.register(r'timedtweets', TimedTweetViewSet)
router.register(r'periodictweets', PeriodicTweetViewSet)
router.register(r'posttweetsets', PostTweetSetViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )
