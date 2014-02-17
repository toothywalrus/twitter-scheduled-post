from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from .views import TweetViewSet, TimedTweetViewSet, \
    PeriodicTweetViewSet, PostTweetSetViewSet, TweetTimedTweetsList, \
    InfoView

router = DefaultRouter(trailing_slash=False)
router.register(r'tweets', TweetViewSet)
router.register(r'timedtweets', TimedTweetViewSet)
router.register(r'periodictweets', PeriodicTweetViewSet)
router.register(r'posttweetsets', PostTweetSetViewSet)

urlpatterns = patterns('',
                       url(r'^tweets/(?P<pk>\d+)/timedtweets$',
                           TweetTimedTweetsList.as_view(
                           ), name='timedtweet-list'),
                       url(r'^info$', InfoView.as_view(), name='info'),
                       url(r'^', include(router.urls)),
                       )
