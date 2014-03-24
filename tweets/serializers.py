from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Tweet, TimedTweet, PeriodicTweet, PostTweetSet,\
    Interval, TwitterUser


class PostableMixin(object):
    already_posted = serializers.SerializerMethodField('is_posted')

    def is_posted(self):
        return None


class TwitterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TwitterUser
        fields = ('id', 'username')


class IntervalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interval


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet


class TimedTweetSerializer(serializers.ModelSerializer):
    # already_posted = serializers.SerializerMethodField('is_posted')

    class Meta:
        model = TimedTweet


class PeriodicTweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = PeriodicTweet


class PostTweetSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostTweetSet
        fields = ('id', 'interval', 'description', 'start_time', 'users')
