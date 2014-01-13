from django.shortcuts import render_to_response
from django.template import RequestContext

from rest_framework import viewsets

from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet
from .serializers import TweetSerializer, TimedTweetSerializer, \
    PeriodicTweetSerializer, PostTweetSetSerializer


def MainHomePage(request):
    context = {'tweets': [1, 2, 3]}
    return render_to_response('index.html', context,
                              context_instance=RequestContext(request))


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class TimedTweetViewSet(viewsets.ModelViewSet):
    queryset = TimedTweet.objects.all()
    serializer_class = TimedTweetSerializer


class PeriodicTweetViewSet(viewsets.ModelViewSet):
    queryset = PeriodicTweet.objects.all()
    serializer_class = PeriodicTweetSerializer


class PostTweetSetViewSet(viewsets.ModelViewSet):
    queryset = PostTweetSet.objects.all()
    serializer_class = PostTweetSetSerializer
